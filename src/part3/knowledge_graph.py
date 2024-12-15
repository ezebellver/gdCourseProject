import csv

import rdflib
from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD
from iribaker import to_iri

# data = 'http://localhost/igd/resource/'
# DATA = Namespace(data)
#
# vocab = 'http://localhost/igd/vocab/'
# VOCAB = Namespace('http://localhost/igd/vocab/')
#
# graph_uri = URIRef('http://localhost/igd/resource/courseproject')
#
# dataset = Dataset()
# dataset.bind('igd', DATA)
# dataset.bind('igd', VOCAB)
#
# graph = dataset.graph(graph_uri)

g = rdflib.Graph()

MOVIE = URIRef("http://localhost/movie/")
USER = URIRef("http://localhost/user/")
ACTOR = URIRef("http://localhost/actor/")
GENRE = URIRef("http://localhost/genre/")

EX = rdflib.Namespace("http://localhost/")


def add_movie_triples(movie_data):
    movie_uri = URIRef(to_iri(MOVIE + movie_data["imdbId"]))
    g.add((movie_uri, rdflib.RDF.type, EX.Movie))
    g.add((movie_uri, RDF.type, EX.Movie))
    g.add((movie_uri, EX.title, Literal(movie_data["title"])))
    g.add((movie_uri, EX.year, Literal(movie_data["year"])))
    g.add((movie_uri, EX.imdbRating, Literal(movie_data["imdbRating"])))
    g.add((movie_uri, EX.runtime, Literal(movie_data["runtime"])))


def add_user_triples(user_data):
    user_uri = URIRef(to_iri(USER + user_data["userId"]))
    g.add((user_uri, RDF.type, EX.User))
    g.add((user_uri, EX.name, rdflib.Literal(user_data["name"])))


def add_actor_triples(actor_data):
    actor_uri = URIRef(to_iri(ACTOR + actor_data["imdbId"]))
    g.add((actor_uri, RDF.type, EX.Actor))
    g.add((actor_uri, EX.name, rdflib.Literal(actor_data["name"])))
    g.add((actor_uri, EX.birthYear, rdflib.Literal(actor_data["birthYear"])))


def add_relationship_triples():
    with open("data/in_genre.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie_uri = URIRef(to_iri(MOVIE + row["movie_imdb_id"]))
            genre_uri = URIRef(to_iri(GENRE + row["genre_name"]))
            g.add((movie_uri, EX.hasGenre, genre_uri))

    with open("data/acted_in.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            actor_uri = URIRef(to_iri(MOVIE + row["actor_imdb_id"]))
            movie_uri = URIRef(to_iri(MOVIE + row["movie_imdb_id"]))
            g.add((actor_uri, EX.actedIn, movie_uri))


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

add_relationship_triples()

g.serialize(destination="knowledge_graph.rdf", format="turtle")

print("RDF knowledge graph has been created and saved as 'knowledge_graph.rdf'")
