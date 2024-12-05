from neo4j_connector import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def recommend_movies(db, user_name, max_year, min_year, max_duration, num_recommendations=10):
    query = """
    MATCH (u:User {name: $user_name})-[:RATED]->(m1:Movie)
    MATCH (m2:Movie)
    WHERE m1 <> m2
    WITH 
        m1, m2,
        abs(m1.imdbRating - m2.imdbRating) / 10 AS rating_sim,
        abs(m1.year - m2.year) / ($max_year - $min_year) AS year_sim,
        abs(m1.duration - m2.duration) / $max_duration AS duration_sim
    WITH 
        m1, m2,
        (0.6 * rating_sim) + (0.3 * year_sim) + (0.1 * duration_sim) AS similarity
    ORDER BY similarity ASC
    LIMIT $num_recommendations
    RETURN m2.title AS recommended_movie, similarity
    """
    recommendations, _, _ = db.execute_query(query, {
        "user_name": user_name,
        "max_year": max_year,
        "min_year": min_year,
        "max_duration": max_duration,
        "num_recommendations": num_recommendations
    })

    return recommendations


if __name__ == "__main__":
    # Create the Neo4j database connection
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    