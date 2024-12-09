from neo4j import GraphDatabase
import csv

# Connect to the Neo4j database
uri = "bolt://localhost:7687"  # Adjust to your Neo4j connection details
user = "neo4j"
password = "password"
driver = GraphDatabase.driver(uri, auth=(user, password))

def export_csv(query, filename):
    with driver.session() as session:
        result = session.run(query)
        # Write the result to a CSV file
        with open(f"data/{filename}", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(result.keys())  # Writing headers
            for record in result:
                writer.writerow(record.values())

# 1. Export Movies data
export_csv("""
MATCH (m:Movie)
RETURN m.title AS title, m.year AS year, m.imdbRating AS imdbRating, m.duration AS duration, m.genres AS genres
""", "movies.csv")

# 2. Export Users data
export_csv("""
MATCH (u:User)
RETURN u.name AS name, u.age AS age, u.gender AS gender
""", "users.csv")

# 3. Export Actors data
export_csv("""
MATCH (a:Actor)
RETURN a.name AS name, a.birthYear AS birthYear, a.nationality AS nationality
""", "actors.csv")

# 4. Export IN_GENRE relationships
export_csv("""
MATCH (m:Movie)-[:IN_GENRE]->(g:Genre)
RETURN m.title AS movie_title, g.name AS genre_name
""", "in_genre.csv")

# 5. Export ACTED_IN relationships
export_csv("""
MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
RETURN a.name AS actor_name, m.title AS movie_title
""", "acted_in.csv")
