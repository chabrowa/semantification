from SPARQLWrapper import SPARQLWrapper, JSON

from approach.config.paths import *
from approach.config.imports import *

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
        query = "select ?s ?p ?o where { \
            ?s ?p ?o . \
            ?s rdf:type <" + self.predictionUrl + "> . \
            filter (isNumeric(?o)) \
            filter (?p != <http://dbpedia.org/ontology/wikiPageID>) \
            filter (?p != <http://dbpedia.org/ontology/wikiPageRevisionID>) \
            }"

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return self.createValuesObject(results["results"]["bindings"])

    def createValuesObject(self, results):
        valuesObject = {}
        for result in results:
            sValue = self.getProperty(result["s"]["value"])
            pValue = self.getProperty(str(result["p"]["value"]))
            oValue = float(result["o"]["value"])
            #spValue = sValue+':'+pValue
            if pValue not in valuesObject:
                valuesObject[pValue] = []
            valuesObject[pValue].append(oValue)
        return 1

    def getProperty(self, numericalProperty):
        return numericalProperty[28:]
