
from approach.config.paths import *
from approach.config.imports import *

from approach.ValuesBag import ValuesBag

class BackgroundKnowledge(object):

    def __init__(self, datasetId, predictions):
        self.datasetId    = datasetId
        self.predictions  = predictions
        self.valuesBags = self.getValuesBags()

    def getValuesBags(self):
        valuesBags = []
        for index, prediction in enumerate(self.predictions):
            valuesBags.append(ValuesBag(prediction[0], prediction[1]))

        return valuesBags
