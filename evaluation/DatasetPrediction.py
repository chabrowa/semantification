from approach.config.paths import *
from approach.config.imports import *

from approach.Semantification import Semantification
from approach.Dataset import Dataset

class DatasetPrediction(object):

    def __init__(self, datasetPath):
        self.datasetPath       = datasetPath
        self.scores            = self.getScores()


    def checkDataset(self, dataset):
        #print dataset.size
        if dataset.size > 2:
            return True
        else:
            return False


    def getScores(self):
        dataset = Dataset(self.datasetPath , 0, [1])
        if self.checkDataset(dataset.df) == False:
            return -1

        sem = Semantification(dataset)
        scores = {}
        scores['columnResults']   = sem.columnsResultsKS
        scores['rowResults']      = sem.rowPredictions
        scores['finalResults']    = sem.finalResults

        print dataset.datasetId
        print list(dataset.df.columns.values)
        print scores['finalResults']
        print "-----------------------------------"
        return scores
