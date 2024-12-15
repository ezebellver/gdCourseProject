from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from src.lib.neo4j_connector import Neo4jConnector


def rate_movies(db, user_name, num_movies=200):
    query = """
    MATCH (m:Movie)
    WHERE m.imdbRating IS NOT NULL AND m.imdbVotes IS NOT NULL
    WITH m.movieId AS movieId, m.imdbRating AS imdbRating
    ORDER BY m.imdbVotes DESC
    LIMIT $num_movies

    WITH movieId, imdbRating, (rand() * 2 - 1) AS variation

    WITH movieId, imdbRating, 
         CASE
             WHEN (imdbRating + variation) < 1 THEN 1
             WHEN (imdbRating + variation) > 10 THEN 10
             ELSE (imdbRating + variation)
         END AS user_rating

    WITH movieId, ROUND(user_rating, 1) AS final_rating

    MERGE (u:User {name: $user_name})
    WITH u, movieId, final_rating

    MATCH (m:Movie {movieId: movieId})
    MERGE (u)-[r:RATED]->(m)
    SET r.rating = final_rating
    WITH m, r
    RETURN m.imdbId AS imdbId, m.title AS title, r.rating AS rating
    ORDER BY r.rating DESC
    """
    result, _, _ = db.execute_query(query, {
        "num_movies": num_movies,
        "user_name": user_name
    })
    for movie in result:
        print(f"User '{user_name}' rated movie '{movie['title']}' ({movie['imdbId']}) with rating {movie['rating']}")


if __name__ == "__main__":
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    user_name = "Sancho Panza"

    rate_movies(db, user_name, num_movies=200)

    db.close()
