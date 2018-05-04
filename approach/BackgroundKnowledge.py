
from approach.config.paths import *
from approach.config.imports import *

from approach.ValuesBag import ValuesBag
from approach.EntityBag import EntityBag

class BackgroundKnowledge(object):

    def __init__(self, datasetId, typePredictions, cellPredictions):
        self.datasetId    = datasetId
        self.typePredictions  = typePredictions
        self.cellPredictions  = cellPredictions
        self.valuesBags = self.getValuesBags()
        self.entityBags = self.getEntityBags()

    def getValuesBags(self):
        valuesBags = []
        counter = 0
        for index, prediction in enumerate(self.typePredictions):
            if counter < noMaxTopPredictions:
                if prediction[1] > minPopularity:
		    print "we are here!!!!!!"
                    valuesBags.append(ValuesBag(prediction[0], prediction[1]))
                    counter += counter

        return valuesBags

    def getEntityBags(self):
        entityBags = []
        for index, prediction in enumerate(self.cellPredictions):
            entityBags.append(EntityBag(prediction.uri, prediction.cell))

        return entityBags
