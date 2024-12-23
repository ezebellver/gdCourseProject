import csv

from iribaker import to_iri
from rdflib import Dataset, URIRef, Literal, Namespace, RDF, RDFS, OWL, XSD


data = 'http://localhost/sancho/resource/'
DATA = Namespace(data)

vocab = 'http://localhost/sancho/vocab/'
VOCAB = Namespace('http://localhost/sancho/vocab/')

graph_uri = URIRef('http://localhost/sancho/resource/examplegraph')

dataset = Dataset()
dataset.bind('data', DATA)
dataset.bind('vocab', VOCAB)

graph = dataset.graph(graph_uri)


def add_movie_triples(movie_data):
    movie = URIRef(to_iri(data + movie_data["imdbId"]))
    dataset.add((movie, RDFS.label, Literal(movie_data["title"])))
    dataset.add((movie, RDF.type, VOCAB['Movie']))
    graph.add((movie, VOCAB["title"], Literal(movie_data["title"])))
    graph.add((movie, VOCAB["year"], Literal(movie_data["year"])))
    graph.add((movie, VOCAB["imdbRating"], Literal(movie_data["imdbRating"])))
    graph.add((movie, VOCAB["runtime"], Literal(movie_data["runtime"])))


def add_user_triples(user_data):
    user = URIRef(to_iri(data + user_data["name"]))
    dataset.add((user, RDFS.label, Literal(user_data["name"])))
    dataset.add((user, RDF.type, VOCAB['User']))
    graph.add((user, VOCAB["name"], Literal(user_data["name"])))


def add_actor_triples(actor_data):
    actor = URIRef(to_iri(data + actor_data["imdbId"]))
    dataset.add((actor, RDFS.label, Literal(actor_data["imdbId"])))
    dataset.add((actor, RDF.type, VOCAB['Actor']))
    graph.add((actor, VOCAB["name"], Literal(actor_data["name"])))
    graph.add((actor, VOCAB["birthYear"], Literal(actor_data["birthYear"])))


def add_relationship_triples():
    with open("data/in_genre.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movie = URIRef(to_iri(data + row["movie_imdb_id"]))
            genre_uri = URIRef(to_iri(data + row["genre_name"]))
            graph.add((movie, VOCAB["hasGenre"], genre_uri))

    with open("data/acted_in.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            actor_uri = URIRef(to_iri(data + row["actor_imdb_id"]))
            movie = URIRef(to_iri(data + row["movie_imdb_id"]))
            graph.add((actor_uri, VOCAB["actedIn"], movie))

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

graph.serialize(destination="data/knowledge_graph.rdf", format="turtle")
