from neo4j import GraphDatabase


class Neo4jConnector:
    """Handles connection to Neo4j database."""

    def __init__(self, uri, user, password, database="courseProject2024.db"):
        """
        Initialize the Neo4j connection.

        :param uri: Bolt URI for the Neo4j instance (e.g., bolt://localhost:7687)
        :param user: Username for authentication
        :param password: Password for authentication
        :param database: Name of the database to connect to
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        """Close the Neo4j connection."""
        self.driver.close()

    def execute_query(self, query, parameters=None):
        """
        Execute a Cypher query on the specified database.

        :param query: The Cypher query to run
        :param parameters: Parameters for the Cypher query
        :return: Tuple (records, summary, keys)
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(query, parameters)
            records = [record.data() for record in result]
            summary = result._summary
            keys = result.keys()
            return records, summary, keys
