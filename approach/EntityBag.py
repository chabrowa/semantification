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


        #print query
        #sparql = SPARQLWrapper("http://wdaqua-csv2rdf-fuseki.univ-st-etienne.fr/dbpedia/query")
        #sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        #sparql = SPARQLWrapper("http://35.198.64.247:8165/sparql")
        #sparql = SPARQLWrapper("http://localhost:23456/db-test/query")
        #sparql = SPARQLWrapper("http://localhost:3031/db-test/query")

        #sparql = SPARQLWrapper("http://uk.dbpedia.org/sparql")
        #sparql = SPARQLWrapper("http://ec2-34-241-15-85.eu-west-1.compute.amazonaws.com/sparql")
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")


        #sparql = SPARQLWrapper("http://kbox.kaist.ac.kr:5889/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        time.sleep(0.5)

        #print "entity"

        return self.createValuesObject(results["results"]["bindings"])

    def createValuesObject(self, results):
        valuesObject = {}
        #valuesObjectClean = {}
        for result in results:
            #pValue = self.getProperty(result["p"]["value"])
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
