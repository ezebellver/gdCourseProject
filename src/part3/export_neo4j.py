from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from src.lib.neo4j_connector import Neo4jConnector


def export_data(db):
    db.export_csv("""
    MATCH (m:Movie)
    RETURN m.imdbId AS imdbId, m.title AS title, m.year AS year, m.imdbRating AS imdbRating, m.runtime AS runtime
    """, "movies.csv")

    db.export_csv("""
    MATCH (u:User)
    RETURN u.name AS name, u.userId AS userId
    """, "users.csv")

    db.export_csv("""
    MATCH (a:Actor)
    RETURN a.name AS name, a.born AS birthYear, a.imdbId as imdbId
    """, "actors.csv")

    db.export_csv("""
    MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
    RETURN m.imdbId as movie_imdb_id, m.title AS movie_title, g.name AS genre_name
    """, "in_genre.csv")

    db.export_csv("""
    MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
    RETURN a.imdbId as actor_imdb_id, a.name AS actor_name, m.title AS movie_title, m.imdbId AS movie_imdb_id
    """, "acted_in.csv")


if __name__ == '__main__':
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    export_data(db)
