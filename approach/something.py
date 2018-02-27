from SPARQLWrapper import SPARQLWrapper, JSON

from approach.config.paths import *
from approach.config.imports import *


entity = "http://dbpedia.org/resource/Makin_(islands)"
query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> select * where { \
            <" + entity + "> ?p ?o . \
            filter (isNumeric(?o)) \
            filter (?p != <http://dbpedia.org/ontology/wikiPageID>) \
            filter (?p != <http://dbpedia.org/ontology/wikiPageRevisionID>) \
            }"

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

sparql.setQuery(query)  # the previous query as a literal string
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

valuesObject = {}
    #valuesObjectClean = {}
for result in results["results"]["bindings"]:
    #pValue = self.getProperty(result["p"]["value"])
    pValue = result["p"]["value"]
    oValue = float(result["o"]["value"])
    if pValue not in valuesObject:
        valuesObject[pValue] = []
    valuesObject[pValue].append(oValue)