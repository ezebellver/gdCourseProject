import os

# Set environment variables manually (if needed for testing or temporary configuration)
os.environ['NEO4J_URI'] = 'bolt://localhost:7687'
os.environ['NEO4J_USER'] = 'neo4j'
os.environ['NEO4J_PASSWORD'] = 'password'
os.environ['OMDB_API_KEY'] = '4b5e7e78'
os.environ['TMDB_API_KEY'] = '382b0ad7fef87dcfe297fbdd65320da8'
os.environ['TMDB_API_RA_KEY'] = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzODJiMGFkN2ZlZjg3ZGNmZTI5N2ZiZGQ2NTMyMGRhOCIsIm5iZiI6MTczMjcwODUwMi44NDA1NDk3LCJzdWIiOiI2NzQ3MDdmMjk1YzU1YTIwMjcxN2ExMDIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.Y0w1EY-tjyGwrBg8W-cUaUftgi-dcTLxIGxR6CAWIcE'

# Neo4j Configuration
NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')    # Neo4j connection URI, default port is 7687
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")                  # Neo4j username (default is 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password')       # Neo4j password (replace with your actual password)

# OMDb API Configuration
OMDB_API_KEY = os.getenv('OMDB_API_KEY')  # OMDb API key
OMDB_API_URL = "http://www.omdbapi.com"  # Base URL for the OMDb API

# TMDb API Configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY')     # TMDb API key
TMDB_API_RA_KEY = os.getenv('TMDB_API_RA_KEY')  # TMDb Read-Access API key
TMDB_API_URL = "https://api.themoviedb.org/3"

# General Project Configuration
RDF_OUTPUT_PATH = "data/rdf_graph.csv"           # Path for exporting the RDF data
SPARQL_QUERIES_PATH = "data/rdf_queries.sparql"  # Path for SPARQL query file
SIMILARITY_THRESHOLD = 0.7                       # Threshold for similarity score (used in recommendations)
BATCH_SIZE = 100                                 # Batch size for handling movie updates (for performance)
