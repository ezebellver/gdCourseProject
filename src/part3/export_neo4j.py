import csv
import os

from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from src.lib.neo4j_connector import Neo4jConnector


def export_to_csv(records, keys, filename):
    if not os.path.exists("data"):
        os.makedirs("data")

    with open(f"data/{filename}", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(keys)
        for record in records:
            writer.writerow(record.values())


def export_data(db):
    query = """
    MATCH (m:Movie)
    WHERE m.imdbId IS NOT NULL AND m.imdbRating IS NOT NULL
    RETURN m.imdbId AS imdbId, m.title AS title, 
           m.year AS year, m.imdbRating AS imdbRating, m.runtime AS runtime
    ORDER BY m.imdbRating DESC
    LIMIT 100
    """

    movies, _, keys = db.execute_query(query)
    export_to_csv(movies, keys, "movies.csv")

    db.export_csv("""
    MATCH (u:User)
    WHERE u.name IS NOT NULL OR u.name = "Sancho Panza"
    RETURN u.name AS name, u.userId AS userId
    LIMIT 30
    """, "users.csv")

    # users, _, keys = db.execute_query(query)
    # export_to_csv(users, keys, "users.csv")

    query = """
    MATCH (a:Actor)
    WHERE a.imdbId IS NOT NULL
    RETURN a.name AS name, a.born AS birthYear, a.imdbId as imdbId
    LIMIT 200
    """

    actors, _, keys = db.execute_query(query)
    export_to_csv(actors, keys, "actors.csv")

    query ="""
    MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
    WHERE m.imdbId IN $movieImdbIds
    RETURN m.imdbId as movie_imdb_id, m.title AS movie_title, g.name AS genre_name
    """

    movie_imdb_ids = [movie["imdbId"] for movie in movies]
    in_genre, _, keys = db.execute_query(query, {"movieImdbIds": movie_imdb_ids})
    export_to_csv(in_genre, keys, "in_genre.csv")

    query = """
    MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
    WHERE a.imdbId IN $actorImdbIds AND m.imdbId IN $movieImdbIds
    RETURN a.imdbId as actor_imdb_id, a.name AS actor_name, m.title AS movie_title, m.imdbId AS movie_imdb_id
    """

    actor_imdb_ids = [actor["imdbId"] for actor in actors]
    acted_in, _, keys = db.execute_query(query, {"actorImdbIds": actor_imdb_ids, "movieImdbIds": movie_imdb_ids})
    export_to_csv(acted_in, keys, "acted_in.csv")


if __name__ == '__main__':
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)



    export_data(db)
