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

        # iterate over values in a numerical column in a dataset
        for i, cell in enumerate(self.dataset.subjectColumn.columnValues):
            # iterate over every baf in entity bags
            for index, bag in enumerate(self.backgroundKnowledge.entityBags):
                if bag.cell == cell:
                    # bag.values is {u'http://dbpedia.org/ontology/squadNumber': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0]}
                    if bag.entity != -1 and bag.values != -1:

                        for val in bag.values:
                            # compare to every value from properties with multiple scores e.q. squadNumber
                            for num in bag.values[val]:
                                columnPredictions.append([cell, bag.entity, val, num, self.sm.relativeDifference(num, self.dataset.getCellValue(columnId, cell))])

        predictionsSorted = sorted(columnPredictions, key=itemgetter(4))
        return predictionsSorted


    def getRowResults(self, rowPredictions):
        rowResults = {}
        # TODO test those prints with two numerical columns
        # for each numerical column
        for column in rowPredictions:
            rowResults[column] = {}
            # for each row in this column
            counter = 1
            for p in enumerate(rowPredictions[column]):
                propertyName = self.getPropertyName(p[1][2])
                prediction = p[1][4]
                #print prediction
                if propertyName not in rowResults[column]:
                    #rowResults[column][propertyName] = prediction
                    rowResults[column][propertyName] = (prediction, [counter])
                else:
                    # we want the best prediction for each property since there can be more than one per property

                    #if rowResults[column][propertyName] > prediction:
                    #    rowResults[column][propertyName] = prediction
                    (pred, arr) = rowResults[column][propertyName]
                    arr.append(counter)
                    if pred > prediction:
                        rowResults[column][propertyName] = (prediction, arr)
                #print rowResults[column]
                counter += 1

            for label in rowResults[column]:
                (pred, arr) = rowResults[column][label]
                rowResults[column][label] = (pred, np.mean(arr))

            rowResults[column] = rowResults[column].items()
            rowResults[column].sort(key=lambda x: (x[1][0], -x[1][1]))

        return rowResults

    def getFinalResults(self):
        finalResults = {}
        columnLevel = self.columnsResultsKS
        rowLevel = self.rowPredictions
        columnsNumber = len(rowLevel)

        #for column in range(1, columnsNumber+1):
        for columnResults in enumerate(rowLevel):
            (iterator, column) = columnResults
            finalResults[column] = {}
            for rowPrediction in enumerate(rowLevel[column]):
                (p, d) = rowPrediction[1]
                finalResults[column][p] = d
            for columnPrediction in enumerate(columnLevel[column]):
                (p, d) = columnPrediction[1]
                if p not in finalResults[column]:
                    finalResults[column][p] = ((1 - d), -1)
                else:
                    (pred, position) = finalResults[column][p]
                    if pred > (1 - d):
                        finalResults[column][p] = ((1 - d), -1)
            finalResults[column] = sorted(finalResults[column].items(), key=lambda x: x[1])

        return finalResults

    def getPropertyName(self, fullProperty):
        return fullProperty[28:]
