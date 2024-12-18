# **Course Project**

## How to Run the Project:

### Prerequisites:

* Docker.
* Python 3.8 or higher.
* OMDb API key (register at OMDb API).

### Steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ezebellver/gdCourseProject
   cd gdCourseProject
   ```

2. **Create a venv and activate it**
    - Windows:
    ```bash
    python -m venv .venv
    call .venv/Scripts/activate
    ```
    - Linux:
    ```bash
    python -m venv .venv
    source bin/activate
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Neo4j**
    - Create a folder called `neo4j/data` and `neo4j/import` in the root of the repository.
    - Place the `courseProject2024.db` file in the `neo4j/import` directory.

5. **Start Neo4j using Docker**
   ```bash
   docker compose up -d
   ```
   
6. **Create a `.env` file in `src/.env`**
    - Windows
    ```env
    set NEO4J_URI=bolt://localhost:7687
    set NEO4J_USER=neo4j
    set NEO4J_PASSWORD=password
    set NEO4J_DATABASE=courseproject2024.db
    set OMDB_API_KEY=<OMDB_API_KEY>
    ```
    - Linux
    ```env
    NEO4J_URI=bolt://localhost:7687
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=password
    NEO4J_DATABASE=courseproject2024.db
    OMDB_API_KEY=<OMDB_API_KEY>
    ```

7. **Source the `.env` file**
    - Windows
    ```bash
    call src/.env
    ```
    - Linux
    ```bash
    source src/.env
    ```

8. **Export PYTHON_PATH variable**
    - Windows
    ```bash
    set PYTHONPATH=%cd%
    ```
    - Linux
    ```bash
    export PYTHONPATH="$PWD"
    ```

#### Part 1

1. **Run the Graph Preparation script**
    ```bash
    python src/part1/graph_preparation.py
    ```

2. **Run the Rate Movies script**
    ```bash
    python src/part1/rate_movies.py
    ```
   
#### Part 2

1. **Run the Recommendation System**
    ```bash
    python src/part2/recommendations.py
    ```

2. **Perform Community Detection**
    ```bash
    python src/part2/community_detection.py
    ```

#### Part 3

1. **Export Neo4j data**
    ```bash
    python src/part3/export_neo4j.py
    ```
   
2. **Export RDF Graph and Validate**
    ```bash
    python src/part3/knowledge_graph.py
    ```

---

## Results

### Part I - Graph Preparation
- Loaded the `courseProject.db` graph into Neo4j.
- Enriched missing `imdbRating` properties for over 5,000 nodes using the OMDb API.
- Added a user node (`Sancho Panza`) with 200 rated movies.

### Part II - Recommendations and Clustering
- Computed similarity scores based on:
  - Numeric properties: `imdbRating`, `year`, and `duration`.
  - Non-numeric properties: Genre overlap.
- Created similarity edges for the 10% most similar movies.
- Detected communities using Louvain and k-means clustering.

#### Louvain Clustering
The Louvain algorithm is a community detection method used to identify clusters within a graph based on modularity optimization. Modularity measures the density of edges within clusters compared to edges between clusters. Louvain works iteratively to maximize modularity, dynamically adjusting nodes to identify the optimal community structure.

**In our application**, we used Louvain clustering to group users into communities based on their interactions (ratings) with movies. This provides insight into user preferences and helps to identify clusters of users with similar movie tastes.

#### K-Means Clustering
K-Means is a machine learning algorithm that partitions data points into a predefined number of clusters (`k`) by minimizing the variance within each cluster. It iteratively assigns points to the nearest cluster center and recalculates the centers until convergence.

**In our application**, we performed K-Means clustering on users using the `ratingCount` property (number of rated movies). This allowed us to segment users into clusters based on their activity levels, providing another dimension for understanding user behavior and tailoring recommendations.

Both approaches complement each other, with Louvain leveraging graph-based community detection and K-Means focusing on numeric feature clustering.

### Part III - Knowledge Graph
- Exported 100 movies, 30 users, 200 actors, and relevant relationships (IN_GENRE and ACTED_IN) to RDF.
- Created CSV files for RDF population in the `data/` folder:
  - `movies.csv`
  - `users.csv`
  - `actors.csv`
  - `in_genre.csv`
  - `acted_in.csv`
- Validated the RDF graph with SPARQL queries placed in the `sparql_queries/` folder:
  - `top_movies.sparql`: List the ten movies with the highest IMDb rating.
  - `movies_by_actor.sparql`: Find movies acted in by "Buster Keaton."
  - `genres_of_movie.sparql`: List genres of the movie "Seven Samurai."
  - `most_common_genres_in_top_movies.sparql`: Count the genres appearing in the top 50 rated movies, grouped and ordered by frequency in descending order.

---

## Group Members

- **Ezequiel Bellver**
- **Santiago Lo Coco**
