import csv
import os

from neo4j import GraphDatabase


class Neo4jConnector:
    def __init__(self, uri, user, password, database="courseProject2024.db"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def execute_query(self, query, parameters=None):
        with self.driver.session(database=self.database) as session:
            result = session.run(query, parameters)
            records = [record.data() for record in result]
            summary = result._summary
            keys = result.keys()
            return records, summary, keys

    def export_csv(self, query, filename):
        with self.driver.session() as session:
            result = session.run(query)
            if not os.path.exists("data"):
                os.makedirs("data")
            with open(f"data/{filename}", "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(result.keys())
                for record in result:
                    writer.writerow(record.values())
