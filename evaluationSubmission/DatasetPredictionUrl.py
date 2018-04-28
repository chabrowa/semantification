from approach.config.paths import *
from approach.config.imports import *

from approach.Semantification import Semantification
from approach.Dataset import Dataset

class DatasetPrediction(object):

    def __init__(self, datasetPath):
        self.datasetPath   = datasetPath
        self.columnMapping = self.getColumnMapping()
        self.scores        = self.getScores()


    def checkDataset(self, dataset):
        if dataset.size > 2:
            return True
        else:
            return False

    # why this is here?
    # def checkCorrect(self, scores):
    #     correctMapping =  self.getPropertyName(self.columnMapping[1])
    #
    #     counter = 0
    #     for prediction in enumerate(scores[2]):
    #         if counter <= 2:
    #             (p,d) = prediction[1]
    #             #if correctMapping != p:
    #                 #print self.datasetPath
    #                 #print correctMapping
    #                 #print scores
    #             counter = counter + 1

    def getScores(self):
        # predefined where are numerical and subject columns
        dataset = Dataset(self.datasetPath, 0, [2])
        if self.checkDataset(dataset.df) == False:
            return -1

        correctProperty = self.getCorrectPrediction()
        # overwriting column type with a correct type  & cell types
        dataset.subjectColumn.columnTypes = [(correctProperty,1)]
        for cell in dataset.subjectColumn.cellPredictions:
            #print cell.cell
            cell.uri   = cell.cell
            cell.types = correctProperty

        sem = Semantification(dataset)
        scores = {}
        scores['columnResults']   = sem.columnsResultsKS
        scores['rowResults']      = sem.rowPredictions
        scores['finalResults']    = sem.finalResults

        #self.checkCorrect(scores['finalResults'])

        return scores

    #correct columns mappings
    def getColumnMapping(self):
        dataset = Dataset(self.datasetPath , 0, [2])
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
