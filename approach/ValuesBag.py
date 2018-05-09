from SPARQLWrapper import SPARQLWrapper, JSON

from approach.config.paths import *
from approach.config.imports import *
#import socket

class ValuesBag(object):

    def __init__(self, prediction, popularity):
        self.prediction    = prediction
        self.popularity    = popularity
        self.predictionUrl = self.getPredictionUrl()
        self.values        = self.getValues()

    def getPredictionUrl(self):
        temp = self.prediction.split(":")
        prediction = temp[1]
        return "http://dbpedia.org/ontology/"+ str(prediction)

    def getValues(self):
        query = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\
             PREFIX owl: <http://www.w3.org/2002/07/owl#>\
             PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> select ?s ?p ?o where { \
             ?s rdf:type <" + self.predictionUrl + "> . \
             ?s ?p ?o . \
             filter(EXISTS{?p rdf:type owl:DatatypeProperty}) \
             filter (?p != <http://dbpedia.org/ontology/wikiPageID>) \
             filter (?p != <http://dbpedia.org/ontology/wikiPageRevisionID>) \
             } LIMIT 10000"

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)
        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()

        return self.createValuesObject(results["results"]["bindings"])

    def createValuesObject(self, results):
        valuesObject = {}
        valuesObjectClean = {}
        for result in results:
            sValue = self.getProperty(result["s"]["value"])
            pValue = self.getProperty(result["p"]["value"])
            try:
                oValue = float(result["o"]["value"])
                if pValue not in valuesObject:
                    valuesObject[pValue] = []
                valuesObject[pValue].append(oValue)
            except:
                pass


        for bag in valuesObject:
            if len(valuesObject[bag]) > 5:
                if bag not in valuesObjectClean:
                    valuesObjectClean[bag] = []
                valuesObjectClean[bag] = valuesObject[bag]
        return valuesObjectClean


    def getProperty(self, numericalProperty):
        return numericalProperty[28:]
