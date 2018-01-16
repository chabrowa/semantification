from approach.BackgroundKnowledge import BackgroundKnowledge
from approach.SimilarityMeasures import SimilarityMeasures

from operator import itemgetter

from approach.config.paths import *
from approach.config.imports import *

class Semantification(object):

    def __init__(self, dataset):
        self.dataset              = dataset
        if self.dataset.subjectColumn != -1:
            self.backgroundKnowledge  = BackgroundKnowledge(self.dataset.datasetId, self.dataset.subjectColumn.columnTypes, self.dataset.subjectColumn.cellPredictions)
        else:
            self.backgroundKnowledge = -1
        self.sm                     = SimilarityMeasures()
        self.columnsPredictionsKS   = self.getColumnsPredictionsKS()
        self.columnsResultsKS       = self.getColumnsResultsKS()
        self.rowPredictions         = self.getRowPredictions()
        self.finalResults           = self.getFinalResults()


    def getColumnsPredictionsKS(self):
        if self.backgroundKnowledge == -1:
            return -1

        mappingResults = {}
        #for i, mappingId in enumerate(self.dataset.columnsWithMappingsIds):
        for j, numericalId in enumerate(self.dataset.numericalColumnsIds):
            #if mappingId == numericalId:
            predictions = self.getColumnPredictions(numericalId)
            mappingResults[numericalId] = predictions
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

        columnsResultsFull = {}
        for index, val in enumerate(self.columnsPredictionsKS):
            columnsResultsFull[val] = {}
            column = self.columnsPredictionsKS[val]
            for i, prediction in enumerate(column):
                (D,p) = prediction[2]
                if prediction[1] not in columnsResultsFull[val]:
                    columnsResultsFull[val][prediction[1]] = p
                else:
                    if columnsResultsFull[val][prediction[1]] < p:
                        columnsResultsFull[val][prediction[1]] = p
            columnsResultsFull[val] = sorted(columnsResultsFull[val].items(), key=operator.itemgetter(1), reverse=True)

        return columnsResultsFull

    def getRowPredictions(self):
        if self.backgroundKnowledge == -1:
            return -1

        rowPredictions = {}
        for j, numericalId in enumerate(self.dataset.numericalColumnsIds):
            predictions = self.getRowPrediction(numericalId)
            rowPredictions[numericalId] = predictions
        return self.getRowResults(rowPredictions)

    def getRowPrediction(self, columnId):
        columnPredictions = []

        for i, cell in enumerate(self.dataset.subjectColumn.columnValues):
            for index, bag in enumerate(self.backgroundKnowledge.entityBags):
                if bag.cell == cell:
                    if bag.entity != -1 and bag.values != -1:
                        for val in bag.values:
                            for num in bag.values[val]:
                                columnPredictions.append([cell, bag.entity, val, num, self.sm.relativeDifference(num, self.dataset.getCellValue(columnId, cell))])

        predictionsSorted = sorted(columnPredictions, key=itemgetter(4))
        return predictionsSorted


    def getRowResults(self, rowPredictions):
        rowResults = {}
        # TODO test those prints with two numerical columns
        for column in rowPredictions:
            rowResults[column] = {}
            for p in enumerate(rowPredictions[column]):
                propertyName = self.getPropertyName(p[1][2])
                prediction = p[1][4]
                if propertyName not in rowResults[column]:
                    rowResults[column][propertyName] = prediction
                else:
                    if rowResults[column][propertyName] > prediction:
                        rowResults[column][propertyName] = prediction

            rowResults[column] = sorted(rowResults[column].items(), key=operator.itemgetter(1))

        return rowResults

    def getFinalResults(self):
        finalResults = {}
        columnLevel = self.columnsResultsKS
        rowLevel = self.rowPredictions
        columnsNumber = len(rowLevel)

        for column in range(1, columnsNumber+1):
            finalResults[column] = {}
            for rowPrediction in enumerate(rowLevel[column]):
                (p, d) = rowPrediction[1]
                finalResults[column][p] = d
            for columnPrediction in enumerate(columnLevel[column]):
                (p, d) = columnPrediction[1]
                if p not in finalResults[column]:
                    finalResults[column][p] = (1 - d)
                else:
                    if finalResults[column][p] > (1 - d):
                        finalResults[column][p] = (1 - d)
            finalResults[column] = sorted(finalResults[column].items(), key=operator.itemgetter(1))

        return finalResults


    def getPropertyName(self, fullProperty):
        return fullProperty[28:]
