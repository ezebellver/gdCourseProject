import pandas as pd

from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from src.lib.neo4j_connector import Neo4jConnector


def perform_louvain_clustering(db):
    query = """
    CALL gds.louvain.write(
        'userMovieGraph',
        {
            writeProperty: 'community'
        }
    )
    YIELD communityCount, modularity
    RETURN communityCount, modularity
    """
    result, _, _ = db.execute_query(query)
    return result


def community_setup(db):
    query = """
        MATCH (u:User)
        WHERE u.ratingCount IS NULL
        OPTIONAL MATCH (u)-[r:RATED]->(m:Movie)
        WITH u, COALESCE(count(r), 0) AS ratingCount
        SET u.ratingCount = [toFloat(ratingCount)]
    """
    db.execute_query(query)

    query = """
        MATCH (u:User)
        OPTIONAL MATCH (u)-[r:RATED]->(m:Movie)
        RETURN gds.graph.project(
            'userMovieGraph',
            u,
            m,
            {
                relationshipProperties: r { .rating }
            }
        )
    """
    db.execute_query(query)

    query = """
    MATCH (u:User)
    RETURN gds.graph.project(
        'userGraph',
        u,
        null,
        {
            sourceNodeProperties: u { .ratingCount },
            targetNodeProperties: {}
        }
    )
    """
    db.execute_query(query)


def community_cleanup(db):
    db.execute_query("CALL gds.graph.drop('userMovieGraph')")
    db.execute_query("CALL gds.graph.drop('userGraph')")


def perform_kmeans_clustering_neo4j(db, n_clusters=5):
    query = f"""
        CALL gds.kmeans.write(
            'userGraph',
            {{
                nodeProperty: 'ratingCount',
                writeProperty: 'kmeansCluster',
                k: {n_clusters},
                randomSeed: 42
            }}
        )
        YIELD nodePropertiesWritten
        RETURN nodePropertiesWritten
    """
    result, _, _ = db.execute_query(query)
    return result


def report_communities_louvain(db):
    query = """
    MATCH (u:User)
    RETURN u.userId AS user, u.community AS community
    ORDER BY community
    """
    results, _, _ = db.execute_query(query)

    df = pd.DataFrame(results)
    return df


def report_communities_kmeans_neo4j(db):
    query = """
    MATCH (u:User)
    RETURN u.userId AS user, u.kmeansCluster AS cluster
    ORDER BY cluster
    """
    results, _, _ = db.execute_query(query)

    df = pd.DataFrame(results)
    return df


if __name__ == "__main__":
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)

    community_setup(db)

    print("Performing Louvain Clustering on Users Based on Rated Movies...")
    louvain_results = perform_louvain_clustering(db)
    print(f"Louvain Clustering Results: {louvain_results}")

    louvain_communities = report_communities_louvain(db)
    print("Louvain Communities for Users (Based on Movie Ratings):")
    print(louvain_communities)

    print("Performing K-Means Clustering on Users Based on Rated Movies...")
    kmeans_results = perform_kmeans_clustering_neo4j(db, n_clusters=5)
    print(f"K-Means Clustering Results: {kmeans_results}")

    kmeans_communities = report_communities_kmeans_neo4j(db)
    print("K-Means Communities for Users (Based on Movie Ratings):")
    print(kmeans_communities)

    community_cleanup(db)
