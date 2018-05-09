from SPARQLWrapper import SPARQLWrapper, JSON

from approach.config.paths import *
from approach.config.imports import *

class EntityBag(object):

    def __init__(self, entity, cell):
        self.cell          = cell
        self.entity        = entity
        self.values        = self.getEntityTriples()

    def getEntityTriples(self):
        if self.entity == -1:
            return -1

        query = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\
                PREFIX owl: <http://www.w3.org/2002/07/owl#> select * where { \
                <" + self.entity + "> ?p ?o . \
                filter(EXISTS{?p rdf:type owl:DatatypeProperty}) \
                filter (?p != <http://dbpedia.org/ontology/wikiPageID>) \
                filter (?p != <http://dbpedia.org/ontology/wikiPageRevisionID>) \
                }"

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query) 
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return self.createValuesObject(results["results"]["bindings"])

    def createValuesObject(self, results):
        valuesObject = {}
        for result in results:
            pValue = result["p"]["value"]
            try:
                oValue = float(result["o"]["value"])
                if pValue not in valuesObject:
                    valuesObject[pValue] = []
                valuesObject[pValue].append(oValue)
            except:
                pass

        return valuesObject

    def getProperty(self, numericalProperty):
        return numericalProperty[28:]
