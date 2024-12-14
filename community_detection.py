from neo4j_connector import Neo4jConnector
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
import pandas as pd


def perform_louvain_clustering(db):
    # Step 1: Use Neo4j Graph Data Science (GDS) for Louvain clustering
    query = """
    CALL gds.graph.project(
        'movieGraph',
        ['Movie', 'User'],
        {
            SIMILAR_TO: {
                properties: 'similarity'
            }
        }
    )
    """
    db.execute_query(query)

    # Step 2: Run the Louvain algorithm
    query = """
    CALL gds.louvain.write(
        'movieGraph',
        {
            writeProperty: 'community'
        }
    )
    YIELD communityCount, modularity
    RETURN communityCount, modularity
    """
    result = db.execute_query(query)
    return result


def perform_kmeans_clustering_neo4j(db, n_clusters=5):
    # Step 1: Create a graph projection if not already done
    query = """
    CALL gds.graph.project(
        'movieGraph',
        ['Movie', 'User'],
        {
            SIMILAR_TO: {
                properties: 'similarity'
            }
        }
    )
    """
    db.execute_query(query)

    # Step 2: Run the K-Means algorithm using Neo4j GDS
    query = f"""
    CALL gds.kmeans.write(
        'movieGraph',
        {{
            nodeProperties: ['similarity'],
            writeProperty: 'kmeansCluster',
            k: {n_clusters}
        }}
    )
    YIELD iterationCount, computeMillis
    RETURN iterationCount, computeMillis
    """
    result = db.execute_query(query)
    return result


def report_communities_louvain(db):
    # Query to fetch communities after Louvain clustering
    query = """
    MATCH (m:Movie)
    RETURN m.title AS movie, m.community AS community
    ORDER BY community
    """
    results = db.execute_query(query)

    # Convert results into a pandas DataFrame for better analysis
    df = pd.DataFrame(results)
    return df


def report_communities_kmeans_neo4j(db):
    # Query to fetch cluster assignments from the graph
    query = """
    MATCH (m:Movie)
    RETURN m.title AS movie, m.kmeansCluster AS cluster
    ORDER BY cluster
    """
    results = db.execute_query(query)

    # Convert results into a pandas DataFrame for better analysis
    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    # Connect to Neo4j
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    # Step 1: Perform Louvain Clustering
    print("Performing Louvain Clustering...")
    louvain_results = perform_louvain_clustering(db)
    print(f"Louvain Clustering Results: {louvain_results}")

    # Fetch and report Louvain communities
    louvain_communities = report_communities_louvain(db)
    print("Louvain Communities:")
    print(louvain_communities)

    # Step 2: Perform K-Means Clustering using Neo4j
    print("Performing K-Means Clustering with Neo4j...")
    kmeans_results = perform_kmeans_clustering_neo4j(db, n_clusters=5)
    print(f"K-Means Clustering Results: {kmeans_results}")

    # Fetch and report K-Means communities
    kmeans_communities = report_communities_kmeans_neo4j(db)
    print("K-Means Communities:")
    print(kmeans_communities)

    # Cleanup: Drop the GDS graph projection to avoid clutter
    db.execute_query("CALL gds.graph.drop('movieGraph')")
