import requests

from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE, OMDB_API_KEY, OMDB_API_URL
from src.lib.neo4j_connector import Neo4jConnector
from src.lib.utils import extract_runtime


def get_movie_details_from_omdb(imdb_id):
    """Fetch the movie information from OMDb API using IMDb ID."""
    url = f"{OMDB_API_URL}/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    return response


def fix_all_movie_ids(db):
    """Fix all movie IMDb IDs that are missing the 'tt' prefix."""
    query = """
    MATCH (m:Movie)
    WHERE m.imdbId IS NOT NULL
    SET m.imdbId = CASE
        WHEN substring(m.imdbId, 0, 2) <> 'tt' THEN 'tt' + m.imdbId
        ELSE m.imdbId
    END
    """
    db.execute_query(query)
    print("Fixed IMDb IDs for all movies.")


def update_movies_without_imdb_rating(db, limit):
    """Find movies without IMDb ratings and update them using the OMDb API."""
    query = """
    MATCH (m:Movie)
    WHERE m.imdbRating IS NULL AND m.imdbId IS NOT NULL
    RETURN m.imdbId AS imdbId
    LIMIT $limit
    """
    movies, _, _ = db.execute_query(query, {"limit": limit})

    for movie in movies:
        imdb_id = movie['imdbId']

        movie_details = get_movie_details_from_omdb(imdb_id)
        print(movie_details)

        if movie_details.get("Response") == "True":
            query_update = """
            MATCH (m:Movie {imdbId: $imdbId})
            SET m.imdbId = $imdbId,
                m.imdbRating = $imdbRating,
                m.imdbVotes = $imdbVotes,
                m.year = $year,
                m.runtime = $runtime
            """
            db.execute_query(query_update, {
                'imdbId': imdb_id,
                'imdbRating': movie_details.get('imdbRating'),
                'imdbVotes': movie_details.get('imdbVotes'),
                'year': movie_details.get('Year'),
                'runtime': extract_runtime(movie_details.get('Runtime'))
            })
            print(f"Updated movie {movie_details.get("Title")} with IMDb ID {imdb_id}")
        else:
            print(f"Failed to fetch details for IMDb ID {imdb_id}")


if __name__ == "__main__":
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE)

    fix_all_movie_ids(db)

    update_movies_without_imdb_rating(db, 5000)

    db.close()
