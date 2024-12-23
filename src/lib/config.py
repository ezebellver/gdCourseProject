import os

NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'neo4j')

OMDB_API_KEY = os.getenv('OMDB_API_KEY')
OMDB_API_URL = "https://www.omdbapi.com"

RDF_OUTPUT_PATH = "part3/data/rdf_graph.csv"
SPARQL_QUERIES_PATH = "part3/data/rdf_queries.sparql"
SIMILARITY_THRESHOLD = 0.7
BATCH_SIZE = 100
