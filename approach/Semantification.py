from approach.BackgroundKnowledge import BackgroundKnowledge
from approach.SimilarityMeasures import SimilarityMeasures

from operator import itemgetter

from approach.config.paths import *
from approach.config.imports import *

class Semantification(object):

    def __init__(self, dataset):
        self.dataset              = dataset
        #print self.dataset.datasetId
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

            #rowResults[column] = sorted(rowResults[column].items(), key=operator.itemgetter(1))
            #print rowResults[column]
            #s = sorted(s, key = lambda x: (x[1], x[2]))
            rowResults[column] = rowResults[column].items()
            rowResults[column].sort(key=lambda x: (x[1][0], -x[1][1]))
            #rowResults[column] = sorted(rowResults[column].items(), key=lambda x: x[1][0])

        return rowResults

    def getFinalResults(self):
        finalResults = {}
        columnLevel = self.columnsResultsKS
        rowLevel = self.rowPredictions
        columnsNumber = len(rowLevel)

        #print self.dataset.datasetId
        #print "Column Level: "
        #print columnLevel
        #print "Row Level: "
        #print rowLevel

        for column in range(1, columnsNumber+1):
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
            #print '-----'
            finalResults[column] = sorted(finalResults[column].items(), key=lambda x: x[1])
            #finalResults[column] = sorted(finalResults[column].items(), key=operator.itemgetter(1))
            #print finalResults[column]
            #print '-------'

        #print "Final Level: "
        #print finalResults

        return finalResults

    #def additionalSorting(self, arr):
        # [(u'minimumElevation', (0.0, 1.5)), (u'longs', (0.34912716829599133, -1)), (u'lats', (0.34912716829599133, -1)), (u'percentageOfAreaWater', (0.34912716829599133, -1)), (u'longm', (0.3696336594414521, -1)), (u'populationDensity', (0.39469177222554308, -1)), (u'latm', (0.41696962235879509, -1)), (u'latd', (0.43305589851086157, -1)), (u'o/wgs84_pos#lat', (0.44058142687915669, -1)), (u'PopulatedPlace/areaTotal', (0.6292134831460674, 9.0)), (u'o/wgs84_pos#long', (0.80565080323029359, -1)), (u'longd', (0.83945483661014497, -1)), (u'elevation', (0.8625, 8.0)), (u'areaWater', (0.87019620363236094, -1)), (u'utcOffset', (0.8787878787878788, 9.0)), (u'blankInfo', (0.91689714020785495, -1)), (u'maximumElevation', (0.9448621553884712, 10.0)), (u'populationTotal', (0.97706587657612665, -1)), (u'populationAsOf', (0.97949601829520572, -1)), (u'areaLand', (0.98161403740627684, -1)), (u'areaTotal', (0.98296423388389942, -1)), (u'PopulatedPlace/area', (1.0, 9.0)), (u'postalCode', (1.0, 10.0)), (u'area', (1.0, 17.0)), (u'PopulatedPlace/populationDensity', (1.0, 19.0))]

        # columnFinalResults = []
        #
        # for (label, scores) in arr:
        #     (prob, accuracy) = scores
        #     if not columnFinalResults:
        #         columnFinalResults.append(label, scores)
        #     else:
        #         lastElementCounter = len(columnFinalResults)
        #         lastElement = columnFinalResults[lastElementCounter-1]
        #         (lastLabel, lastScores) = lastElement
        #         (lastProb, lastAccuracy) = lastScores
        #         if lastProb == prob:
        #             if lastAccuracy == -1:
        #             elif accuracy == -1:
        #             elif lastAccuracy > accuracy:
        #             else:
        #
        #         else:
        #             columnFinalResults.append(label, scores)






    def getPropertyName(self, fullProperty):
        return fullProperty[28:]
