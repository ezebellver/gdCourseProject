import networkx as nx
import community  # Louvain method
import numpy as np
from sklearn.cluster import KMeans
from recommendations import recommend_unrated_movies
from neo4j_connector import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


def louvain_community_detection(db, user_name, genre_list):
    # Step 1: Use the recommend_unrated_movies to get top similar unrated movies
    top_similar_movies = recommend_unrated_movies(db, user_name, genre_list, top_percent=10)

    # Step 2: Build a NetworkX graph from the movie similarity data
    G = nx.Graph()
    for unrated_movie, rated_movie, similarity_score in top_similar_movies:
        G.add_edge(unrated_movie['title'], rated_movie['title'], weight=similarity_score)

    # Step 3: Apply Louvain Community Detection Algorithm
    partition = community.best_partition(G)

    # Step 4: Assign movies to communities
    movie_communities = {}
    for movie, community_id in partition.items():
        movie_communities[movie] = community_id

    # Step 5: Organize communities
    communities = {}
    for movie, community_id in movie_communities.items():
        if community_id not in communities:
            communities[community_id] = []
        communities[community_id].append(movie)

    # Output the communities
    for community_id, movies in communities.items():
        print(f"Community {community_id}: {', '.join(movies)}")

    return communities


def kmeans_clustering(db, user_name, genre_list, num_clusters=5):
    # Step 1: Use the recommend_unrated_movies to get top similar unrated movies
    top_similar_movies = recommend_unrated_movies(db, user_name, genre_list, top_percent=10)

    # Step 2: Create a feature matrix for K-means clustering (using similarity scores as features)
    movie_names = []
    similarity_matrix = []

    for unrated_movie, rated_movie, similarity_score in top_similar_movies:
        movie_names.append((unrated_movie['title'], rated_movie['title']))
        similarity_matrix.append([similarity_score])

    # Convert to numpy array for KMeans
    similarity_matrix = np.array(similarity_matrix)

    # Step 3: Apply K-means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(similarity_matrix)

    # Step 4: Assign movies to clusters
    movie_clusters = {}
    for idx, (movie1_title, movie2_title) in enumerate(movie_names):
        cluster_id = kmeans.labels_[idx]
        if cluster_id not in movie_clusters:
            movie_clusters[cluster_id] = []
        movie_clusters[cluster_id].append((movie1_title, movie2_title))

    # Step 5: Output clusters
    for cluster_id, movie_pairs in movie_clusters.items():
        print(f"Cluster {cluster_id}: {', '.join([f'{m1} & {m2}' for m1, m2 in movie_pairs])}")

    return movie_clusters


def main():
    # Initialize Neo4j connector
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    user_name = "john_doe"  # Replace with the desired user's name
    genre_list = []  # Replace with the list of genres, if needed

    # Louvain Community Detection
    print("Louvain Community Detection:")
    louvain_communities = louvain_community_detection(db, user_name, genre_list)

    # K-Means Clustering
    print("\nK-Means Clustering:")
    kmeans_clusters = kmeans_clustering(db, user_name, genre_list, num_clusters=5)


if __name__ == "__main__":
    main()
