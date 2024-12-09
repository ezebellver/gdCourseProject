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
2. Build a recommendation system based on similarity metrics.
3. Perform community detection using clustering algorithms.
4. Export a portion of the graph as RDF and write SPARQL queries to validate the data.

---

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
* `main.py`: Entry point for running the entire project pipeline.
* `graph_preparation.py`: Handles data loading, cleaning, and enrichment in Neo4j.
* `recommendations.py`: Computes movie recommendations based on similarity metrics (numerical and genre).
* `community_detection.py`: Implements Louvain and k-means clustering for community detection.
* `knowledge_graph.py`: Handles RDF graph creation and SPARQL query validation.

#### Other Files:

* `requirements.txt`: Lists Python dependencies required for the project.


### How to Run the Project:

#### Prerequisites:

* Neo4j version 5.25 installed and running in a Docker container.
* Python 3.8 or higher.
* OMDb API key (register at OMDb API).

#### Steps:

1. Clone the Repository
   ```bash
   git clone [https://github.com/your-repo/courseproject2024.git](https://github.com/your-repo/courseproject2024.git)
   cd courseproject2024```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Neo4j**
    - Place the `courseProject2024.db` file in the Neo4j directory.
    - Configure connection details in `config.py`.

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
- Added a user node (`Added User`) with 200 rated movies.

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

## Contact
For any questions about the project, feel free to contact:
- Ezequiel Bellver
- Santiago Lo Coco