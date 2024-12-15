import pandas as pd

from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from src.lib.neo4j_connector import Neo4jConnector


def perform_louvain_clustering(db):
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
    query = """
    MATCH (m:Movie)
    RETURN m.title AS movie, m.community AS community
    ORDER BY community
    """
    results = db.execute_query(query)

    df = pd.DataFrame(results)
    return df


def report_communities_kmeans_neo4j(db):
    query = """
    MATCH (m:Movie)
    RETURN m.title AS movie, m.kmeansCluster AS cluster
    ORDER BY cluster
    """
    results = db.execute_query(query)

    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    print("Performing Louvain Clustering...")
    louvain_results = perform_louvain_clustering(db)
    print(f"Louvain Clustering Results: {louvain_results}")

    louvain_communities = report_communities_louvain(db)
    print("Louvain Communities:")
    print(louvain_communities)

    print("Performing K-Means Clustering with Neo4j...")
    kmeans_results = perform_kmeans_clustering_neo4j(db, n_clusters=5)
    print(f"K-Means Clustering Results: {kmeans_results}")

    kmeans_communities = report_communities_kmeans_neo4j(db)
    print("K-Means Communities:")
    print(kmeans_communities)

    db.execute_query("CALL gds.graph.drop('movieGraph')")
