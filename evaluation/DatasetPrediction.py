from approach.config.paths import *
from approach.config.imports import *

from evaluation.Semantification import Semantification

class DatasetPrediction(object):

    def __init__(self, datasetPath):
        self.datasetPath       = datasetPath
        self.scores            = self.getScores()


    def getScores(self):
        sem = Semantification(self.datasetPath)
        scores = {}
        scores['columnResults']   = sem.columnsResultsKS
        scores['rowResults']      = sem.rowPredictions
        scores['finalResults']    = sem.finalResults 

        return scores
