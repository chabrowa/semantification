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

    def testLocalFiles(self, newFile):
        for fn in os.listdir(localdatabasePath):
            #print "compare: " + fn + " - " + newFile
            if fn == newFile:
                #print "we are here"
                return True
        return False

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

        fileName = hashlib.md5(query)
        fileName = str(fileName.hexdigest())+".p"
        fileExists = self.testLocalFiles(fileName)
        if fileExists:
            results = pickle.load(open(localdatabasePath+""+fileName, "rb"))
            #print "hurray we are here"
            #print "we are here saving our time"

        else:
            #sparql = SPARQLWrapper("http://wdaqua-csv2rdf-fuseki.univ-st-etienne.fr/dbpedia/query")
            #sparql = SPARQLWrapper("http://35.198.64.247:8165/sparql")
            #sparql = SPARQLWrapper("http://localhost:23456/db-test/query")
            #sparql = SPARQLWrapper("http://localhost:3031/db-test/query")
            #sparql = SPARQLWrapper("http://kbox.kaist.ac.kr:5889/sparql")
            #sparql = SPARQLWrapper("http://ec2-34-241-15-85.eu-west-1.compute.amazonaws.com/sparql")
            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setReturnFormat(JSON)
            #sparql.setTimeout(1200)
            sparql.setQuery(query)  # the previous query as a literal string
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            #time.sleep(0.5)
            pickle.dump(results, open(localdatabasePath+""+fileName, "wb"))
            #print "we dont want to be here"

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
