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

        query = "select * where { \
            <" + self.entity + "> ?p ?o . \
            filter (isNumeric(?o)) \
            }"
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query)  # the previous query as a literal string
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return self.createValuesObject(results["results"]["bindings"])

    def createValuesObject(self, results):
        valuesObject = {}
        #valuesObjectClean = {}
        for result in results:
            #pValue = self.getProperty(result["p"]["value"])
            pValue = result["p"]["value"]
            oValue = float(result["o"]["value"])
            if pValue not in valuesObject:
                valuesObject[pValue] = []
            valuesObject[pValue].append(oValue)

        # for bag in valuesObject:
        #     if len(valuesObject[bag]) > 5:
        #         if bag not in valuesObjectClean:
        #             valuesObjectClean[bag] = []
        #         valuesObjectClean[bag] = valuesObject[bag]
        # return valuesObjectClean
        return valuesObject

    def getProperty(self, numericalProperty):
        return numericalProperty[28:]
