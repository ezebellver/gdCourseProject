from neo4j_connector import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import numpy as np


def calculate_numerical_similarity(movie1, movie2):
    # Define normalization ranges
    imdb_min, imdb_max = 0, 10
    year_min, year_max = 1894, 2030
    duration_min, duration_max = 60, 360

    # Normalize the values for IMDb Rating (0-10)
    normalized_rating1 = (movie1['imdbRating'] - imdb_min) / (imdb_max - imdb_min)
    normalized_rating2 = (movie2['imdbRating'] - imdb_min) / (imdb_max - imdb_min)

    # Normalize the values for Year (1894-2030)
    # 1894 is the oldest film in IMDb
    normalized_year1 = (movie1['year'] - year_min) / (year_max - year_min)
    normalized_year2 = (movie2['year'] - year_min) / (year_max - year_min)

    # Normalize the values for Duration (60-360)
    normalized_duration1 = (movie1['duration'] - duration_min) / (duration_max - duration_min)
    normalized_duration2 = (movie2['duration'] - duration_min) / (duration_max - duration_min)

    # Calculate the squared differences for each feature
    rating_diff_squared = (normalized_rating1 - normalized_rating2) ** 2
    year_diff_squared = (normalized_year1 - normalized_year2) ** 2
    duration_diff_squared = (normalized_duration1 - normalized_duration2) ** 2

    # Apply weights to the squared differences (lower differences mean higher similarity)
    weighted_diff = (0.6 * rating_diff_squared) + (0.3 * year_diff_squared) + (0.1 * duration_diff_squared)

    # Calculate the Euclidean distance (this is the final similarity score)
    similarity_score = np.sqrt(weighted_diff)

    # Return the similarity score (lower is more similar)
    return similarity_score


def calculate_genre_similarity(movie1, movie2):
    # Get the genre sets for both movies
    genres1 = set(movie1['genres'])
    genres2 = set(movie2['genres'])

    # Calculate the intersection and union of the genre sets
    intersection = len(genres1.intersection(genres2))
    union = len(genres1.union(genres2))

    # Return the Jaccard similarity (intersection / union)
    if union == 0:  # Prevent division by zero if both movies have no genres
        return 0
    return intersection / union


def get_all_movie_pairs(db, user_name):
    # Query to get the movies rated by the user
    query = """
    MATCH (u:User {name: $user_name})-[:RATED]->(m1:Movie)
    MATCH (m2:Movie)
    WHERE m1 <> m2
    RETURN m1, m2
    """
    movie_pairs = db.execute_query(query, {"user_name": user_name})

    return movie_pairs


def compute_all_similarities(movie_pairs, genre_list):
    similarity_scores = []

    for m1, m2 in movie_pairs:
        # Compute similarity between the two movies
        numerical_similarity = calculate_numerical_similarity(m1, m2)  # Using Euclidean similarity
        genre_similarity = calculate_genre_similarity(m1, m2)  # Using Jaccard similarity

        # Combine numerical and genre similarity (weighted)
        combined_similarity = (0.6 * numerical_similarity) + (0.4 * genre_similarity)

        # Append similarity score and movie pair
        similarity_scores.append((m1['title'], m2['title'], combined_similarity))

    return similarity_scores


def select_top_similar_movies(similarity_scores, top_percent=10):
    # Sort similarity scores in descending order (most similar first)
    similarity_scores.sort(key=lambda x: x[2], reverse=True)

    # Select the top 10% most similar movies
    top_similar_count = int(len(similarity_scores) * top_percent / 100)
    top_similar_movies = similarity_scores[:top_similar_count]

    return top_similar_movies


def create_edges_in_graph(db, top_similar_movies):
    for movie1_title, movie2_title, similarity_score in top_similar_movies:
        # Cypher query to create an edge between the two movies with similarity score
        query = """
        MATCH (m1:Movie {title: $movie1_title})
        MATCH (m2:Movie {title: $movie2_title})
        MERGE (m1)-[r:SIMILAR_TO]->(m2)
        SET r.similarity = $similarity_score
        """
        db.execute_query(query, {
            "movie1_title": movie1_title,
            "movie2_title": movie2_title,
            "similarity_score": similarity_score
        })


def get_rated_movies_above_threshold(db, user_name, rating_threshold=8):
    query = """
    MATCH (u:User {name: $user_name})-[:RATED]->(m:Movie)
    WHERE m.imdbRating > $rating_threshold
    RETURN m
    """
    rated_movies = db.execute_query(query, {
        "user_name": user_name,
        "rating_threshold": rating_threshold
    })

    return rated_movies


def get_unrated_movies(db, user_name):
    query = """
    MATCH (u:User {name: $user_name})-[:RATED]->(m:Movie)
    MATCH (m2:Movie)
    WHERE NOT (u)-[:RATED]->(m2)
    RETURN m2
    """
    unrated_movies = db.execute_query(query, {
        "user_name": user_name
    })

    return unrated_movies


def calculate_similarity_to_rated_movies(unrated_movies, rated_movies, genre_list):
    similarity_scores = []

    for unrated_movie in unrated_movies:
        for rated_movie in rated_movies:
            # Compute similarity between the unrated movie and the rated movie
            numerical_similarity = calculate_numerical_similarity(unrated_movie, rated_movie)
            genre_similarity = calculate_genre_similarity(unrated_movie, rated_movie)

            # Combine numerical and genre similarity (weighted)
            combined_similarity = (0.6 * numerical_similarity) + (0.4 * genre_similarity)

            # Append similarity score and movie pair
            similarity_scores.append((unrated_movie['title'], rated_movie['title'], combined_similarity))

    return similarity_scores


def normalize_similarity_score(similarity_score, min_similarity=0, max_similarity=1):
    # Normalize similarity score to be between 0 and 10
    normalized_score = (similarity_score - min_similarity) / (max_similarity - min_similarity) * 10
    return min(10, max(0, normalized_score))  # Ensure it stays between 0 and 10


def select_top_unrated_movies(similarity_scores, top_percent=10):
    # Sort similarity scores in descending order (most similar first)
    similarity_scores.sort(key=lambda x: x[2], reverse=True)

    # Select the top 10% most similar movies
    top_similar_count = int(len(similarity_scores) * top_percent / 100)
    top_similar_movies = similarity_scores[:top_similar_count]

    return top_similar_movies


def recommend_unrated_movies(db, user_name, genre_list, rating_threshold=8, top_percent=10):
    # Step 1: Get rated movies above the threshold
    rated_movies = get_rated_movies_above_threshold(db, user_name, rating_threshold)

    # Step 2: Get unrated movies
    unrated_movies = get_unrated_movies(db, user_name)

    # Step 3: Calculate similarities between unrated movies and rated movies
    similarity_scores = calculate_similarity_to_rated_movies(unrated_movies, rated_movies, genre_list)

    # Step 4: Normalize the similarity scores to the range 0-10
    similarity_scores = [(unrated_movie, rated_movie, normalize_similarity_score(similarity_score))
                         for unrated_movie, rated_movie, similarity_score in similarity_scores]

    # Step 5: Select the top most similar unrated movies
    top_similar_movies = select_top_unrated_movies(similarity_scores, top_percent)

    return top_similar_movies
