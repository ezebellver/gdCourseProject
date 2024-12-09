import os

# Set environment variables manually
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'password'
# os.environ['NEO4J_DATABASE'] = 'courseProject2024.db'
os.environ['NEO4J_DATABASE'] = 'courseproject2024.db'
os.environ['OMDB_API_KEY'] = '4b5e7e78'

# Neo4j Configuration
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')    # Neo4j connection URI, default port is 7687
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")                  # Neo4j username (default is 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')       # Neo4j password (replace with your actual password)
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', 'neo4j')

# OMDb API Configuration
OMDB_API_KEY = os.getenv('OMDB_API_KEY')  # OMDb API key
OMDB_API_URL = "http://www.omdbapi.com"  # Base URL for the OMDb API

# General Project Configuration
RDF_OUTPUT_PATH = "data/rdf_graph.csv"           # Path for exporting the RDF data
SPARQL_QUERIES_PATH = "data/rdf_queries.sparql"  # Path for SPARQL query file
SIMILARITY_THRESHOLD = 0.7                       # Threshold for similarity score (used in recommendations)
BATCH_SIZE = 100                                 # Batch size for handling movie updates (for performance)
