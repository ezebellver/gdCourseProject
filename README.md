# **Course Project**

## **Group Members**
- **Ezequiel Bellver**
- **Santiago Lo Coco**

## **Professor**
- **Alejandro Vaisman**

## **Course Information**
- **Course Code:** MSE-BB-3-WS2024-IGD  
- **Course Name:** Introduction to Graph Databases  
- **University:** FH Technikum Wien (FHTW)

---

## **Project Overview**

This project focuses on working with graph data in a Neo4j database. It involves loading, cleaning, enriching, and analyzing graph data using Python and various tools. The tasks include recommendation systems, community detection, and exporting a portion of the graph as an RDF knowledge graph.

### **Objectives**

1. Prepare a graph database by:
   - Loading the provided graph (`courseproject2024.db`).
   - Enriching the graph with missing `imdbRating` data using an API.
   - Adding a user node with 200 movie ratings.
2. Build a recommendation system based on similarity metrics and perform community detection using clustering algorithms.
3. Export a portion of the graph as RDF and write SPARQL queries to validate the data.

---

### How to Run the Project:

#### Prerequisites:

* Docker.
* Python 3.8 or higher.
* OMDb API key (register at OMDb API).

#### Steps:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ezebellver/gdCourseProject
   cd gdCourseProject
   ```

2. **Create a venv and activate it**
    ```bash
    python -m venv
    call .venv\Scripts\activate
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

4. **Run the Graph Preparation Script**
    ```bash
    python graph_preparation.py
    ```

5. **Run the Recommendation System**
    ```bash
    python recommendations.py
    ```

6. **Perform Community Detection**
    ```bash
    python community_detection.py
    ```

7. **Export RDF Graph and Validate**
    ```bash
    python knowledge_graph.py
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


### Project Files:

#### Directories:

* `data/`
    * `rdf_graph.csv`: Exported graph data for RDF creation.
    * `rdf_queries.sparql`: Contains SPARQL queries for RDF validation.
    * `recommendations.csv`: Contains computed similarity scores for movies.
* `sparql_queries/`
    * `top_movies.sparql`: Query to list the ten movies with the highest IMDb rating.
    * `movies_by_actor.sparql`: Query to find all movies acted in by "Leonardo DiCaprio."
    * `genres_of_inception.sparql`: Query to get all genres associated with the movie "Inception."

#### Code Files:

* `config.py`: Contains configurations for Neo4j and the OMDb API.
* `graph_preparation.py`: Handles data loading, cleaning, and enrichment in Neo4j.
* `recommendations.py`: Computes movie recommendations based on similarity metrics (numerical and genre).
* `community_detection.py`: Implements Louvain and k-means clustering for community detection.
* `knowledge_graph.py`: Handles RDF graph creation and SPARQL query validation.

#### Other Files:

* `requirements.txt`: Lists Python dependencies required for the project.
