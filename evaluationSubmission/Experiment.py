from approach.config.paths import *
from approach.config.imports import *

from evaluationSubmission.DatasetPredictionUrl import DatasetPrediction

class Experiment(object):

    def __init__(self, size, percentageDeviation, dataPath):
        self.size                = size
        self.dataPath            = dataPath
        self.datasetsPredictions = self.getDatasetPredictions()
        #self.datasetsPredictions = self.getNotWorkingDatasetPredictions()
        self.percentageDeviation = percentageDeviation
        self.score               = self.getScore()


    # def getNotWorkingDatasetPredictions(self):
    #     datasetPredictions = []
    #     count = 0
    #
    #     for fn in os.listdir(self.dataPath):
    #         #if fn in sample3:
    #         datasetPath = os.path.join(self.dataPath, fn)
    #         dataset = DatasetPrediction(datasetPath)
    #         if dataset.scores != -1:
    #             datasetPredictions.append(dataset)
    #         count = count + 1
    #         print count
    #     print "all datasets: " + str(count)
    #
    #     return datasetPredictions

    def getDatasetPredictions(self):
        datasetPredictions = []
        count = 0
        for fn in os.listdir(self.dataPath):
            #print str(count) + ":  " + str(fn)
            #if count < 10:
            datasetPath = os.path.join(self.dataPath, fn)
            dataset = DatasetPrediction(datasetPath)
            if dataset.scores != -1:
                datasetPredictions.append(dataset)
            count = count + 1
        print "all datasets: " + str(count)

        return datasetPredictions

    def getScore(self):
        correctlyLabelledTop1 = 0
        correctlyLabelledTop3 = 0
        correctlyLabelledTopX = 0
        total                 = 0

        for datasetPrediction in self.datasetsPredictions:
            total = total + 1
            correctMapping =  self.getPropertyName(datasetPrediction.columnMapping[2])

            # calculating from top 3 predictions
            counter = 0
            finalScores = datasetPrediction.scores['finalResults'][2]
            for prediction in enumerate(finalScores):
                if counter <= 2:
                    (p,d) = prediction[1]
                    if correctMapping == p:
                        correctlyLabelledTop3 = correctlyLabelledTop3 + 1
                counter = counter + 1

            # calculating if any predictions
            for prediction in enumerate(finalScores):
                (p,d) = prediction[1]
                if correctMapping == p:
                    correctlyLabelledTopX = correctlyLabelledTopX + 1
            prediction = finalScores[0]
            (p,d) = prediction
            if correctMapping == p:
                correctlyLabelledTop1 = correctlyLabelledTop1 + 1
            else:
                print "NOT correct mapping: " + str(correctMapping) + " - " + str(p)
                print datasetPrediction.datasetPath
                print finalScores



        print 'top 1 correctly labelled: ' + str(correctlyLabelledTop1)
        print 'top 3 correctly labelled: ' + str(correctlyLabelledTop3)
        print 'top X correctly labelled: ' + str(correctlyLabelledTopX)
        print 'total: ' + str(total)

        return 0

    def getPropertyName(self, fullProperty):
        return fullProperty[28:]
