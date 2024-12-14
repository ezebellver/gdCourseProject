from neo4j_connector import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def calculate_similarities_in_graph(db, user_name, rating_threshold=8, limit=100):
    # Cypher query to calculate similarities between rated and unrated movies
    query = """
    WITH $user_name AS user_name, $rating_threshold AS rating_threshold
    MATCH (u:User {name: user_name})-[:RATED]->(rated:Movie)
    WHERE rated.imdbRating > rating_threshold
    MATCH (unrated:Movie)
    WHERE NOT (u)-[:RATED]->(unrated)
    WITH 
        rated, unrated,
        toFloat(rated.imdbRating) / 10.0 AS normalized_rating_rated,
        toFloat(unrated.imdbRating) / 10.0 AS normalized_rating_unrated,
        ((toFloat(rated.year) - 1894.0) / (2030.0 - 1894.0)) AS normalized_year_rated,
        ((toFloat(unrated.year) - 1894.0) / (2030.0 - 1894.0)) AS normalized_year_unrated,
        ((toFloat(rated.duration) - 60.0) / (360.0 - 60.0)) AS normalized_duration_rated,
        ((toFloat(unrated.duration) - 60.0) / (360.0 - 60.0)) AS normalized_duration_unrated
    WITH 
        unrated,
        rated,
        sqrt(
            0.6 * (normalized_rating_rated - normalized_rating_unrated) ^ 2 +
            0.3 * (normalized_year_rated - normalized_year_unrated) ^ 2 +
            0.1 * (normalized_duration_rated - normalized_duration_unrated) ^ 2
        ) AS numerical_similarity,
        size(
            apoc.coll.intersection(
                apoc.coll.toSet(rated.genres),
                apoc.coll.toSet(unrated.genres)
            )
        ) AS intersection_size,
        size(
            apoc.coll.union(
                apoc.coll.toSet(rated.genres),
                apoc.coll.toSet(unrated.genres)
            )
        ) AS union_size
    WITH 
        unrated,
        rated,
        (0.6 * (1 - numerical_similarity) + 0.4 * (intersection_size / union_size)) AS combined_similarity
    RETURN unrated.title AS unrated_title, rated.title AS rated_title, combined_similarity
    ORDER BY combined_similarity DESC
    LIMIT $limit
    """

    results = db.execute_query(query, {
        "user_name": user_name,
        "rating_threshold": rating_threshold,
        "limit": limit
    })

    return results


def create_similarity_edges_in_graph(db, recommendations):
    # Cypher query to create similarity edges between unrated and rated movies
    query = """
    WITH $recommendations AS recommendations
    UNWIND recommendations AS rec
    MATCH (unrated:Movie {title: rec.unrated_movie})
    MATCH (rated:Movie {title: rec.rated_title})
    MERGE (unrated)-[r:SIMILAR_TO]->(rated)
    SET r.similarity = rec.similarity
    """

    db.execute_query(query, {"recommendations": recommendations})


def recommend_unrated_movies(db, user_name, rating_threshold=8, top_percent=10):
    # Step 1: Calculate Similarities
    similarity_scores = calculate_similarities_in_graph(db, user_name, rating_threshold)

    # Step 2: Process the results to select top recommendations
    similarity_scores.sort(key=lambda x: x['combined_similarity'], reverse=True)
    top_similar_count = int(len(similarity_scores) * top_percent / 100)
    top_similar_movies = similarity_scores[:top_similar_count]

    # Step 3: Prepare the recommendations for creating edges
    recommendations = [
        {
            "unrated_movie": score['unrated_title'],
            "rated_title": score['rated_title'],
            "similarity": score['combined_similarity']
        }
        for score in top_similar_movies
    ]

    return recommendations


if __name__ == "__main__":
    # Connect to Neo4j
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    # Example user and parameters
    user_name = "Project User"
    rating_threshold = 8
    top_percent = 10

    # Step 1: Get recommendations
    recommendations = recommend_unrated_movies(db, user_name, rating_threshold, top_percent)

    # Step 2: Create similarity edges in the graph
    create_similarity_edges_in_graph(db, recommendations)

    # Output recommendations
    for rec in recommendations:
        print(
            f"Unrated Movie: {rec['unrated_movie']}, Most Similar Rated Movie: {rec['rated_title']}, Similarity: {rec['similarity']:.2f}")
