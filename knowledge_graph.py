import rdflib
from rdflib.namespace import RDF, RDFS, URIRef
import csv

# Create a graph instance
g = rdflib.Graph()

# Define namespaces
MOVIE = URIRef("http://localhost/movie/")
USER = URIRef("http://localhost/user/")
ACTOR = URIRef("http://localhost/actor/")
GENRE = URIRef("http://localhost/genre/")


# Helper function to create resources and add triples
def add_movie_triples(movie_data):
    movie_uri = URIRef(MOVIE + movie_data["title"].replace(" ", "_"))
    g.add((movie_uri, RDF.type, MOVIE.Movie))
    g.add((movie_uri, MOVIE.title, rdflib.Literal(movie_data["title"])))
    g.add((movie_uri, MOVIE.year, rdflib.Literal(movie_data["year"])))
    g.add((movie_uri, MOVIE.imdbRating, rdflib.Literal(movie_data["imdbRating"])))
    g.add((movie_uri, MOVIE.duration, rdflib.Literal(movie_data["duration"])))
    for genre in movie_data["genres"]:
        genre_uri = URIRef(GENRE + genre.replace(" ", "_"))
        g.add((movie_uri, MOVIE.hasGenre, genre_uri))


def add_user_triples(user_data):
    user_uri = URIRef(USER + user_data["name"].replace(" ", "_"))
    g.add((user_uri, RDF.type, USER.User))
    g.add((user_uri, USER.name, rdflib.Literal(user_data["name"])))
    g.add((user_uri, USER.age, rdflib.Literal(user_data["age"])))
    g.add((user_uri, USER.gender, rdflib.Literal(user_data["gender"])))


def add_actor_triples(actor_data):
    actor_uri = URIRef(ACTOR + actor_data["name"].replace(" ", "_"))
    g.add((actor_uri, RDF.type, ACTOR.Actor))
    g.add((actor_uri, ACTOR.name, rdflib.Literal(actor_data["name"])))
    g.add((actor_uri, ACTOR.birthYear, rdflib.Literal(actor_data["birthYear"])))
    g.add((actor_uri, ACTOR.nationality, rdflib.Literal(actor_data["nationality"])))


def add_relationship_triples():
    # IN_GENRE relationship
    with open("data/in_genre.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie_uri = URIRef(MOVIE + row["movie_title"].replace(" ", "_"))
            genre_uri = URIRef(GENRE + row["genre_name"].replace(" ", "_"))
            g.add((movie_uri, MOVIE.hasGenre, genre_uri))

    # ACTED_IN relationship
    with open("data/acted_in.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            actor_uri = URIRef(ACTOR + row["actor_name"].replace(" ", "_"))
            movie_uri = URIRef(MOVIE + row["movie_title"].replace(" ", "_"))
            g.add((actor_uri, ACTOR.actedIn, movie_uri))


# Load CSV data into the RDF graph
with open("data/movies.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        add_movie_triples(row)

with open("data/users.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        add_user_triples(row)

with open("data/actors.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        add_actor_triples(row)

# Add relationships
add_relationship_triples()

# Serialize the RDF graph to a file
g.serialize(destination="knowledge_graph.rdf", format="turtle")

print("RDF knowledge graph has been created and saved as 'knowledge_graph.rdf'")
