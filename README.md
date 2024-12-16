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
- Added a user node (`Project User`) with 200 rated movies.

### Part II - Recommendations and Clustering
- Computed similarity scores based on:
  - Numeric properties: `imdbRating`, `year`, and `duration`.
  - Non-numeric properties: Genre overlap.
- Created similarity edges for the 10% most similar movies.
- Detected communities using Louvain and k-means clustering.

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
  - `movies_by_actor.sparql`: Find movies acted in by "Leonardo DiCaprio."
  - `genres_of_inception.sparql`: List genres of the movie "Inception."

---

## Group Members

- **Ezequiel Bellver**
- **Santiago Lo Coco**
