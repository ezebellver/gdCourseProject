import requests
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE, OMDB_API_KEY
from neo4j_connector import Neo4jConnector


def get_movie_details_from_omdb(imdb_id):
    """Fetch detailed movie information from OMDb API using IMDb ID."""
    url = f"http://www.omdbapi.com/?i={imdb_id}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()
    return response


def fix_imdb_id(imdb_id):
    """Ensure IMDb ID has the 'tt' prefix."""
    if not imdb_id.startswith("tt"):
        # Pad the ID with leading zeros and prepend 'tt'
        imdb_id = f"tt{imdb_id.zfill(7)}"
    return imdb_id


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
    # Query to fetch the newest movies missing IMDb ratings, limited to 5000
    query = """
    MATCH (m:Movie)
    WHERE m.imdbRating IS NULL AND m.imdbId IS NOT NULL AND m.year IS NOT NULL
    RETURN m.movieId AS movieId, m.imdbId AS imdbId
    ORDER BY m.year DESC
    LIMIT $limit
    """
    movies, _, _ = db.execute_query(query, {"limit": limit})

    for movie in movies:
        imdb_id = movie['imdbId']  # IMDb ID should now be fixed
        movie_id = movie['movieId']

        # Fetch data from OMDb API
        movie_details = get_movie_details_from_omdb(imdb_id)
        if movie_details.get("Response") == "True":
            # Update the movie node in the database
            query_update = """
            MATCH (m:Movie {movieId: $movie_id})
            SET m.imdbId = $imdbId,
                m.imdbRating = $imdbRating,
                m.imdbVotes = $imdbVotes,
                m.plot = $plot,
                m.awards = $awards,
                m.language = $language,
                m.country = $country,
                m.poster = $poster,
                m.rated = $rated,
                m.released = $released,
                m.runtime = $runtime,
                m.writer = $writer,
                m.metascore = $metascore
            """
            db.execute_query(query_update, {
                'movie_id': movie_id,
                'imdbId': imdb_id,
                'imdbRating': movie_details.get('imdbRating'),
                'imdbVotes': movie_details.get('imdbVotes'),
                'plot': movie_details.get('Plot', ''),
                'awards': movie_details.get('Awards', ''),
                'language': movie_details.get('Language', ''),
                'country': movie_details.get('Country', ''),
                'poster': movie_details.get('Poster', ''),
                'rated': movie_details.get('Rated', ''),
                'released': movie_details.get('Released', ''),
                'runtime': movie_details.get('Runtime', ''),
                'writer': movie_details.get('Writer', ''),
                'metascore': movie_details.get('Metascore', '')
            })
            print(f"Updated movie {movie_id} with IMDb ID {imdb_id}")
        else:
            print(f"Failed to fetch details for IMDb ID {imdb_id}")


if __name__ == "__main__":
    # Create the Neo4j database connection
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE)

    # First, fix all IMDb IDs (ensure correct 'tt' prefix)
    fix_all_movie_ids(db)

    # Then, fix movies without IMDb ratings
    update_movies_without_imdb_rating(db, 5000)

    # Close the database connection when done
    db.close()
