from src.lib.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE, OMDB_API_KEY, OMDB_API_URL
from src.lib.neo4j_connector import Neo4jConnector


def update_movies_with_imdb_rating(db, limit):
    query = """
    CALL apoc.periodic.iterate(
        'MATCH (m:Movie)
        WHERE m.imdbRating IS NULL AND m.imdbId IS NOT NULL
        RETURN m
        LIMIT $limit',
        
        'WITH m, 
             CASE 
                 WHEN NOT m.imdbId STARTS WITH "tt" THEN "tt" + m.imdbId 
                 ELSE m.imdbId 
             END AS fixedImdbId
        SET m.imdbId = fixedImdbId
        WITH m, fixedImdbId AS imdbId
        CALL apoc.load.json($omdbApiUrl + "/?i=" + imdbId + "&apikey=" + $apikey) 
        YIELD value
        SET m.imdbRating = value.imdbRating,
            m.year = value.Year,
            m.runtime = CASE 
                WHEN value.Runtime IS NOT NULL AND value.Runtime <> "N/A" 
                THEN toInteger(SPLIT(value.Runtime, " ")[0]) 
                ELSE NULL 
            END
        RETURN m.title AS title, 
               m.imdbId AS imdbId, 
               m.imdbRating AS imdbRating, 
               m.year AS year, 
               m.runtime AS runtime',
        
        {
            batchSize: 50,
            parallel: true,
            params: {
                omdbApiUrl: $omdbApiUrl,
                apikey: $apikey,
                limit: $limit
            }
        }
    )
    """
    updated, _, _ = db.execute_query(query, {
        "omdbApiUrl": OMDB_API_URL,
        "apikey": OMDB_API_KEY,
        "limit": limit
    })
    print(updated)


if __name__ == "__main__":
    db = Neo4jConnector(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, NEO4J_DATABASE)

    update_movies_with_imdb_rating(db, 5000)

    # Note that the API has a limit of 1000 requests per day with the free tier.
    # Therefore, the above function will not work for more than 1000 movies at once.
    # However, you can run this script multiple times, each time with a limit of 1000.
    # update_movies_with_imdb_rating(db, 1000)

    db.close()
