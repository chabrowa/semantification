from approach.Dataset import Dataset
from approach.BackgroundKnowledge import BackgroundKnowledge
from approach.SimilarityMeasures import SimilarityMeasures

from approach.config.paths import *
from approach.config.imports import *

class Semantification(object):

    def __init__(self, datasetId):
        self.dataset              = Dataset(datasetId)
        if self.dataset.subjectColumn != -1:
            self.backgroundKnowledge  = BackgroundKnowledge(datasetId, self.dataset.subjectColumn.columnTypes)
        else:
            self.backgroundKnowledge = -1
        self.sm                     = SimilarityMeasures()
        self.columnsPredictionsKS   = self.getColumnsPredictionsKS()
        self.columnsResultsKS       = self.getColumnsResultsKS()


    def getColumnsPredictionsKS(self):
        if self.backgroundKnowledge == -1:
            return -1

        mappingResults = {}
        for i, mappingId in enumerate(self.dataset.columnsWithMappingsIds):
            for j, numericalId in enumerate(self.dataset.numericalColumnsIds):
                if mappingId == numericalId:
                    predictions = self.getColumnPredictions(numericalId)
                    mappingResults[mappingId] = predictions
                    #if prediction == self.dataset.columnsWithMappings[mappingId]:
                    #print predictions
        #print mappingResults
        return mappingResults

    def getColumnPredictions(self, columnId):
        columnPredictions = []
        for index, bag in enumerate(self.backgroundKnowledge.valuesBags):
            for key, values in bag.values.iteritems():
                columnPredictions.append([bag.prediction ,key, self.sm.KSTest(self.dataset.getColumnValues(columnId), values)])
        return columnPredictions

    def getColumnsResultsKS(self):
        if self.backgroundKnowledge == -1:
            return -1
        columnsResults = {}
        for index, val in enumerate(self.columnsPredictionsKS):
            highestP = 0
            column = self.columnsPredictionsKS[val]
            for i, prediction in enumerate(column):
                #print prediction
                #print "______________________"
                (D,p) = prediction[2]
                if p > highestP:
                    highestP = p
                    highestLabel = prediction[1]
                    propertyName = prediction[0]
            columnsResults[val] = [propertyName, highestLabel, highestP]
        print self.dataset.datasetId
        print columnsResults
        return columnsResults
