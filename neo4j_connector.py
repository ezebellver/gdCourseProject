from neo4j import GraphDatabase


class Neo4jConnector:
    """Handles connection to Neo4j database."""

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        """Close the Neo4j connection."""
        self.driver.close()

    def execute_query(self, query, parameters=None):
        """Execute a Cypher query."""
        with self.driver.session() as session:
            result = session.run(query, parameters)
            records = [record.data() for record in result]
            summary = result._summary
            keys = result.keys()
            return records, summary, keys
