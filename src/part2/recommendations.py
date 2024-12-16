from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from src.lib.neo4j_connector import Neo4jConnector


def calculate_similarities_in_graph(db, limit):
    query = """
    MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec:Movie)
    WHERE m.imdbRating IS NOT NULL AND 
        m.year IS NOT NULL AND m.runtime IS NOT NULL AND 
        rec.imdbRating IS NOT NULL AND rec.year IS NOT NULL 
        AND rec.runtime IS NOT NULL AND m.title <> rec.title
    WITH m, rec
    LIMIT $limit

    MATCH (m)-[:IN_GENRE]->(g:Genre)<-[:IN_GENRE]-(rec)
    WITH m, rec,
        abs(toFloat(m.imdbRating) - toFloat(rec.imdbRating)) AS ratingDiff,
        abs(toFloat(m.year) - toFloat(rec.year)) AS yearDiff,
        abs(toFloat(m.runtime) - toFloat(rec.runtime)) AS durationDiff,
        count(g) AS genreScore

    WITH m, rec, genreScore,
        (1/(1 + ratingDiff)) * 0.5 + (1/(1 + yearDiff)) * 0.3 + (1/(1 + durationDiff)) * 0.2 AS numericScore
    WITH m, rec, (numericScore + genreScore * 0.5) / 1.5 AS totalScore

    ORDER BY m.title, totalScore DESC
    WITH m, collect(rec) AS recommendations, totalScore
    WITH m, recommendations[..toInteger(ceil(size(recommendations) * 0.1))] AS topRecommendations, totalScore

    UNWIND topRecommendations AS rec
    MERGE (m)-[:SIMILAR {score: totalScore}]->(rec);
    """

    results = db.execute_query(query, {
        "limit": limit
    })

    return results


def get_recommendations(db, user_name):
    query = """
    MATCH (u:User {name: $user_name})-[r:RATED]->(m:Movie)
    WHERE r.rating >= 8
    MATCH (m)-[s:SIMILAR]->(rec:Movie)
    WHERE NOT (u)-[:RATED]->(rec)
    RETURN rec, m, r.rating AS userRating, s.score AS similarityScore
    ORDER BY similarityScore DESC
    """

    results, _, _ = db.execute_query(query, {"user_name": user_name})

    return results



def recommend_unrated_movies(db, user_name, limit):
    calculate_similarities_in_graph(db, limit)
    print("Similarity scores calculated")

    recommendations = get_recommendations(db, user_name)
    print("Recommendations fetched")

    return recommendations

if __name__ == "__main__":
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    user_name = "Sancho Panza"

    recommendations = recommend_unrated_movies(db, user_name, 1000000)
    
    for record in recommendations:
        print(f"Movie: '{record['rec']['title']}', score: '{record['similarityScore']}'")
        print(f"Based on movie: '{record['m']['title']}', user rating: '{record['userRating']}'")
