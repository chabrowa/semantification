#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import random
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import csv


class dbpediaQuery(object):

    def __init__(self, fileIn):
        self.counter = 0
        self.fileIn = fileIn
        # self.fileOut = fileOut
        self.propertyList = self.fileOpener()
        self.meanUse = {}
        self.medianUse = {}
        self.maxUse = {}
        self.minUse = {}
        # self.fileWriter(self.sameAsList)

    def fileOpener(self):
        resultList = []
        with open(self.fileIn, 'r') as f:
            for line in f:
                propertyClean = line.strip()
                resultList.append(propertyClean)

        return resultList

    def getValues(self):
        propertyUseData = {}
        for dbProperty in self.propertyList:
            query = "SELECT DISTINCT ?class (COUNT(?o) AS ?noStats) WHERE " \
                    "{?s <"+dbProperty+"> ?o ." \
                    " ?s a ?class . } GROUP BY ?class"

            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setReturnFormat(JSON)

            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            resultsProcessed = self.propertyHandler(results, dbProperty)
            propertyUseData[dbProperty] = resultsProcessed

            # valueJoined = '\n'.join(self.createValuesObject(results["results"]["bindings"], self.WDItem))
        return propertyUseData

    def getTables(self, dbClass, dbProperty):

            query = "SELECT ?s ?o WHERE {?s <"+dbProperty+"> ?o . ?s a <"+dbClass+"> . FILTER(isNumeric(?o))} "

            sparql = SPARQLWrapper("http://dbpedia.org/sparql")
            sparql.setReturnFormat(JSON)

            sparql.setQuery(query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
            self.tableDataHandler(results, dbClass, dbProperty)

            return results

    def propertyHandler(self, results, prop):
        propertyUses = {}
        discardedClasses = ['http://dbpedia.org/ontology/Agent'] #'http://dbpedia.org/ontology/Person' ?
        for result in results["results"]["bindings"]:
            if result['class']['value'].startswith('http://dbpedia.org/ontology'):
                if result['class']['value'] not in discardedClasses:
                    dbClass = result['class']['value']
                try:
                    noTriples = result['noStats']['value']
                    propertyUses[dbClass] = int(noTriples)
                except KeyError:
                    print result

        classesSelected = self.classesSelector(propertyUses, prop)

        return classesSelected

    def tableDataHandler(self, results, dbclass, prop):
        self.counter += 1
        fileName = prop.replace('http://dbpedia.org/ontology/', 'dbo_') + '-' + str(self.counter) + '.csv'
        with open(fileName, 'w') as csvfile:
            tableWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            tableWriter.writerow([dbclass.encode('utf-8'), prop.encode('utf-8')])

            for result in results["results"]["bindings"]:
                subj = result['s']['value']
                obj = result['o']['value']
                tableWriter.writerow([subj.encode('utf-8'), obj.encode('utf-8')])


    def classesSelector(self, dicto, prop):
        valueList = [dicto[key] for key in dicto]
        self.meanUse[prop] = np.mean(valueList)
        self.medianUse[prop] = np.median(valueList)
        self.maxUse[prop] = np.max(valueList)
        self.minUse[prop] = np.min(valueList)
        try:
            chosenOnes = random.sample([key for key in dicto], 10)
        except ValueError:
            chosenOnes = [key for key in dicto]

        ### Use these if you want to get only classes in the 5-95 quantiles
        # lowerQuantile = np.percentile(valueList, 5)
        # upperQuantile = np.percentile(valueList, 95)
        # toBeDeleted = [key for key in dicto if dicto[key] < lowerQuantile and dicto[key] > upperQuantile]
        # for k in toBeDeleted:
        #     dicto.pop(k, None)
        # chosenOnes = random.sample([key for key in dicto if dicto[key] > lowerQuantile and dicto[key] < upperQuantile], 3)


        return chosenOnes


    def processTables(self, dbClasses):
        for key in dbClasses.keys():
            for value in dbClasses[key]:
                self.getTables(value, key)



def main():
    file_name = sys.argv[1]
    # file_output = sys.argv[2]
    x = dbpediaQuery(file_name)
    propList = x.getValues()
    x.processTables(propList)

if __name__ == "__main__":
    main()