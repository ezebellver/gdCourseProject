import networkx as nx
import community  # Louvain method
import numpy as np
from sklearn.cluster import KMeans
from neo4j_connector import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def calculate_numerical_similarity(movie1, movie2):
    # Define normalization ranges
    imdb_min, imdb_max = 0, 10
    year_min, year_max = 1894, 2030
    duration_min, duration_max = 60, 360

    # Normalize the values for IMDb Rating (0-10)
    normalized_rating1 = (movie1['imdbRating'] - imdb_min) / (imdb_max - imdb_min)
    normalized_rating2 = (movie2['imdbRating'] - imdb_min) / (imdb_max - imdb_min)

    # Normalize the values for Year (1894-2030)
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


def louvain_community_detection(db):
    # Step 1: Get graph data from Neo4j (user-to-movie similarity graph or user connections)
    query = """
    MATCH (u:User)-[:RATED]->(m:Movie)<-[:RATED]-(other:User)
    RETURN u.name AS user1, other.name AS user2, 1 AS weight
    """
    edges = db.execute_query(query)

    # Step 2: Create a NetworkX graph from the query results
    G = nx.Graph()
    for edge in edges:
        user1, user2, weight = edge
        G.add_edge(user1, user2, weight=weight)

    # Step 3: Apply Louvain Community Detection Algorithm
    partition = community.best_partition(G)

    # Step 4: Assign users to communities
    user_communities = {}
    for user, community_id in partition.items():
        user_communities[user] = community_id

    # Step 5: Print out the communities
    communities = {}
    for user, community_id in user_communities.items():
        if community_id not in communities:
            communities[community_id] = []
        communities[community_id].append(user)

    # Output the communities
    for community_id, users in communities.items():
        print(f"Community {community_id}: {', '.join(users)}")

    return communities


def kmeans_clustering(db, num_clusters=5):
    # Step 1: Get movie ratings data for users
    query = """
    MATCH (u:User)-[:RATED]->(m:Movie)
    RETURN u.name AS user, COLLECT(m.title) AS movies, COLLECT(rating) AS ratings
    """
    user_ratings = db.execute_query(query)

    # Step 2: Create a feature matrix based on user ratings (for simplicity, use the number of ratings)
    user_features = []
    user_names = []

    for user_rating in user_ratings:
        user_name = user_rating['user']
        ratings = user_rating['ratings']
        user_names.append(user_name)
        user_features.append([len(ratings)])  # Feature: number of rated movies (simple example)

    # Step 3: Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(user_features)

    # Step 4: Assign users to clusters
    user_clusters = {}
    for idx, user_name in enumerate(user_names):
        cluster_id = kmeans.labels_[idx]
        if cluster_id not in user_clusters:
            user_clusters[cluster_id] = []
        user_clusters[cluster_id].append(user_name)

    # Step 5: Output clusters
    for cluster_id, users in user_clusters.items():
        print(f"Cluster {cluster_id}: {', '.join(users)}")

    return user_clusters


def main():
    # Initialize Neo4j connector
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    # Louvain Community Detection
    print("Louvain Community Detection:")
    louvain_communities = louvain_community_detection(db)

    # K-Means Clustering
    print("\nK-Means Clustering:")
    kmeans_clusters = kmeans_clustering(db, num_clusters=5)


if __name__ == "__main__":
    main()
