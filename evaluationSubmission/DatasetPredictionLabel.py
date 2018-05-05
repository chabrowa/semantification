from approach.config.paths import *
from approach.config.imports import *

from approach.Semantification import Semantification
from approach.Dataset import Dataset

class DatasetPrediction(object):

    def __init__(self, datasetPath):
	self.datasetPath   = datasetPath
        self.columnMapping = self.getColumnMapping()
        self.scores        = self.getScores()
        self.rowsNumber    = self.getRowsNumber()


    def getRowsNumber(self):
        # predefined where are numerical and subject columns
        dataset = Dataset(self.datasetPath , 1, [2])
        if self.checkDataset(dataset.df) == False:
            return -1

        return dataset.df.size

    def checkDataset(self, dataset):
        if dataset.size > 2:
            return True
        else:
            return False


    def getScores(self):
        # predefined where are numerical and subject columns
        dataset = Dataset(self.datasetPath , 1, [2])
        if self.checkDataset(dataset.df) == False:
            return -1

        sem = Semantification(dataset)
        scores = {}
        scores['columnResults']   = sem.columnsResultsKS
        scores['rowResults']      = sem.rowPredictions
        scores['finalResults']    = sem.finalResults

        return scores

    def getColumnMapping(self):
        dataset = Dataset(self.datasetPath , 0, [1])
        if self.checkDataset(dataset.df) == False:
            return -1
        return list(dataset.df.columns.values)


    def getPropertyName(self, fullProperty):
        return fullProperty[28:]

    def getCorrectPrediction(self):
        dataset = pd.read_csv(self.datasetPath)
        propertyList = list(dataset.columns.values)
        # 'DBpedia:Work'
        correctProperty =  "DBpedia:" + self.getPropertyName(propertyList[0])
        return correctProperty
