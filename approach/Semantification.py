from approach.Dataset import Dataset
from approach.BackgroundKnowledge import BackgroundKnowledge
from approach.SimilarityMeasures import SimilarityMeasures

from approach.config.paths import *
from approach.config.imports import *

class Semantification(object):

    def __init__(self, datasetId):
        self.dataset              = Dataset(datasetId)
        self.backgroundKnowledge  = BackgroundKnowledge(datasetId, self.dataset.subjectColumn.columnTypes)
        self.sm                   = SimilarityMeasures()

    def getPredictionsResults(self):
        mappingResults = []
        for i, mappingId in enumerate(self.dataset.columnsWithMappingsIds):
            for j, numericalId in enumerate(self.dataset.numericalColumnsIds):
                if mappingId == numericalId:
                    prediction = self.getColumnPrediction(numericalId)
                    #if prediction == self.dataset.columnsWithMappings[mappingId]:
                    #print prediction

    def getColumnPrediction(self, columnId):
        for index, bag in enumerate(self.backgroundKnowledge.valuesBags):
            for key, values in bag.values.iteritems():
                #print key
                #print values
                #print self.dataset.getColumnValues(columnId)
                print self.sm.KSTest(self.dataset.getColumnValues(columnId), values)

        return 1
