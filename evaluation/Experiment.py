from approach.config.paths import *
from approach.config.imports import *

from evaluation.DatasetPrediction import DatasetPrediction

class Experiment(object):

    def __init__(self, topK, size, percentageDeviation, dataPath):
        self.topK                = topK
        self.size                = size
        self.dataPath            = dataPath
        self.datasetsPredictions = self.getDatasetPredictions()
        self.percentageDeviation = percentageDeviation
        self.score               = self.getScore()

    def getDatasetPredictions(self):
        datasetPredictions = []

        for fn in self.dataPath:
            datasetPath = dataPath + fn
            datasetPredictions.append(DatasetPrediction(datasetPath))

        return datasetPredictions

    def getScore():
        return 0
