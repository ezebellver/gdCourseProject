import random
from decimal import Decimal, ROUND_DOWN
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j_connector import Neo4jConnector


def create_user_node(db, user_name):
    """Create a user node in the Neo4j graph."""
    query = """
    MERGE (u:User {name: $name})
    RETURN u
    """
    db.execute_query(query, {"name": user_name})
    print(f"User node created for '{user_name}'")


def rate_movies(db, user_name, num_movies=200):
    """Rate the top movies with the most IMDb votes for the user."""
    # Fetch the top `num_movies` movies sorted by IMDb votes
    query = """
    MATCH (m:Movie)
    WHERE m.imdbRating IS NOT NULL AND m.imdbVotes IS NOT NULL
    RETURN m.movieId AS movieId, m.imdbRating AS imdbRating
    ORDER BY m.imdbVotes DESC
    LIMIT $num_movies
    """
    movies, _, _ = db.execute_query(query, {"num_movies": num_movies})

    for movie in movies:
        movie_id = movie["movieId"]
        imdb_rating = float(movie["imdbRating"])

        # Add some random variation to the IMDb rating to simulate a user rating
        variation = random.normalvariate(0, 1.0)  # Normal distribution (mean=0, stddev=1)
        user_rating = imdb_rating + variation

        # Ensure the rating stays within the valid range of 1 to 10
        user_rating = max(1, min(10, user_rating))

        # Truncate the rating to 2 decimal places
        user_rating = float(Decimal(user_rating).quantize(Decimal("0.01"), rounding=ROUND_DOWN))

        # Create a "RATED" relationship between the user and the movie
        query_rate = """
        MATCH (u:User {name: $user_name}), (m:Movie {movieId: $movie_id})
        MERGE (u)-[r:RATED]->(m)
        SET r.rating = $rating
        """
        db.execute_query(query_rate, {"user_name": user_name, "movie_id": movie_id, "rating": user_rating})

        print(f"User '{user_name}' rated movie {movie_id} with a rating of {user_rating:.2f}")


if __name__ == "__main__":
    # Create the Neo4j database connection
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    # Ask for the user's name
    user_name = "Project User"

    # Create the user node
    create_user_node(db, user_name)

    # Rate the top 200 movies
    rate_movies(db, user_name, num_movies=200)

    # Close the database connection when done
    db.close()
