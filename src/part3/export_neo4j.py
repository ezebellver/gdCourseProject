from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from src.lib.neo4j_connector import Neo4jConnector


def export_data(db):
    db.export_csv("""
    MATCH (m:Movie)
    RETURN m.title AS title, m.year AS year, m.imdbRating AS imdbRating, m.runtime AS runtime
    """, "movies.csv")

    db.export_csv("""
    MATCH (u:User)
    RETURN u.name AS name, u.userId AS userId
    """, "users.csv")

    db.export_csv("""
    MATCH (a:Actor)
    RETURN a.name AS name, a.born AS birthYear
    """, "actors.csv")

    db.export_csv("""
    MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
    RETURN m.title AS movie_title, g.name AS genre_name
    """, "in_genre.csv")

    db.export_csv("""
    MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
    RETURN a.name AS actor_name, m.title AS movie_title
    """, "acted_in.csv")


if __name__ == '__main__':
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    export_data(db)
