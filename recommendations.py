from neo4j_connector import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def calculate_similarities_in_graph(db, user_name, rating_threshold=8, limit=100):
    # Cypher query to calculate similarities between rated and unrated movies
    query = """
    WITH $user_name AS user_name, $rating_threshold AS rating_threshold
    MATCH (u:User {name: user_name})-[:RATED]->(rated:Movie)
    WHERE rated.imdbRating > rating_threshold
    WITH u, rated LIMIT $limit
    MATCH (unrated:Movie)
    WHERE NOT (u)-[:RATED]->(unrated) AND unrated.imdbRating IS NOT NULL
    WITH unrated, rated
    MATCH (rated)-[:IN_GENRE]->(rated_genre:Genre)
    MATCH (unrated)-[:IN_GENRE]->(unrated_genre:Genre)
    WITH unrated, rated,
        collect(DISTINCT rated_genre.name) AS rated_genres,
        collect(DISTINCT unrated_genre.name) AS unrated_genres,
        coalesce(toFloat(rated.imdbRating), 0.0) / 10.0 AS normalized_rating_rated,
        coalesce(toFloat(unrated.imdbRating), 0.0) / 10.0 AS normalized_rating_unrated,
        coalesce((toFloat(rated.year) - 1894.0) / (2030.0 - 1894.0), 0.0) AS normalized_year_rated,
        coalesce((toFloat(unrated.year) - 1894.0) / (2030.0 - 1894.0), 0.0) AS normalized_year_unrated,
        coalesce((toFloat(rated.runtime) - 60.0) / (360.0 - 60.0), 0.0) AS normalized_runtime_rated,
        coalesce((toFloat(unrated.runtime) - 60.0) / (360.0 - 60.0), 0.0) AS normalized_runtime_unrated
    WITH unrated, rated, rated_genres, unrated_genres,
        sqrt(
            0.6 * (normalized_rating_rated - normalized_rating_unrated) ^ 2 +
            0.3 * (normalized_year_rated - normalized_year_unrated) ^ 2 +
            0.1 * (normalized_runtime_rated - normalized_runtime_unrated) ^ 2
        ) AS numerical_similarity,
        [g IN rated_genres WHERE g IN unrated_genres] AS common_genres,
        size(rated_genres) + size(unrated_genres) - size([g IN rated_genres WHERE g IN unrated_genres]) AS union_size
    WITH unrated, rated,
     CASE 
         WHEN union_size = 0 THEN 0
         ELSE (0.6 * (1 - numerical_similarity) + 0.4 * (size(common_genres) / union_size)) 
     END AS combined_similarity
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
    similarity_scores = calculate_similarities_in_graph(db, user_name, rating_threshold)
    similarity_scores = similarity_scores[0]
    print(similarity_scores)

    similarity_scores.sort(key=lambda x: x['combined_similarity'], reverse=True)
    top_similar_count = int(len(similarity_scores) * top_percent / 100)
    top_similar_movies = similarity_scores[:top_similar_count]

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
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    user_name = "Project User"
    rating_threshold = 8
    top_percent = 10

    recommendations = recommend_unrated_movies(db, user_name, rating_threshold, top_percent)

    create_similarity_edges_in_graph(db, recommendations)

    for rec in recommendations:
        print(
            f"Unrated Movie: {rec['unrated_movie']}, Most Similar Rated Movie: {rec['rated_title']}, Similarity: {rec['similarity']:.2f}")
