from approach.config.paths import *
from approach.config.imports import *

#from evaluationSubmission.DatasetPredictionUrl import DatasetPrediction
from evaluationSubmission.DatasetPredictionLabel import DatasetPrediction

class Experiment(object):

    def __init__(self, size, percentageDeviation, dataPath):
        self.size                = size
        self.dataPath            = dataPath
        self.datasetsPredictions = self.getDatasetPredictions()
        self.percentageDeviation = percentageDeviation

        # Results
        self.levelResults        = self.getLevelScore()
        self.results             = self.getScore()



    def getDatasetPredictions(self):
        datasetPredictions = []
        count = 0
        for fn in os.listdir(self.dataPath):
            #if count < 20:
            #print str(count) + ":  " + str(fn)
            datasetPath = os.path.join(self.dataPath, fn)
            #if fn == "dbo_formationYear-817-smallest.csv":
            if "dbo_formationYear" in fn:
                print str(count) + ":  " + str(fn)
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
            try:
                prediction = finalScores[0]
                (p,d) = prediction
            except:
                prediction = ''
                p = ''
                d = ''

            if correctMapping == p:
                correctlyLabelledTop1 = correctlyLabelledTop1 + 1
            else:
                #pass
                print "NOT correct mapping: " + str(correctMapping) + " - " + str(p)
                print datasetPrediction.datasetPath
                print finalScores
        #
        #
        #
        print " OVERAL ANALYSIS: "
        print 'top 1 correctly labelled: ' + str(correctlyLabelledTop1)
        print 'top 3 correctly labelled: ' + str(correctlyLabelledTop3)
        print 'top X correctly labelled: ' + str(correctlyLabelledTopX)
        print 'total: ' + str(total)

        results = {}
        results['top1']  = correctlyLabelledTop1
        results['top3']  = correctlyLabelledTop3
        results['topX']  = correctlyLabelledTopX
        results['total'] = total

        return results


    def getLevelScore(self):
        results = {}

        # --------------------- COLUMN LEVEL ANALYSIS -----------------------------
        correctlyLabelledTop1Col = 0
        correctlyLabelledTop3Col = 0
        correctlyLabelledTopXCol = 0
        totalCol   = 0

        for datasetPrediction in self.datasetsPredictions:
            totalCol = totalCol + 1
            correctMapping =  self.getPropertyName(datasetPrediction.columnMapping[2])

            # calculating from top 3 predictions
            counter = 0
            # [2] because we are interested in only column 2 in the datasets
            finalScores = datasetPrediction.scores['columnResults'][2]
            for prediction in enumerate(finalScores):
                if counter <= 2:
                    (p,d) = prediction[1]
                    if correctMapping == p:
                        correctlyLabelledTop3Col = correctlyLabelledTop3Col + 1
                counter = counter + 1

            # calculating if any predictions
            for prediction in enumerate(finalScores):
                (p,d) = prediction[1]
                if correctMapping == p:
                    correctlyLabelledTopXCol = correctlyLabelledTopXCol + 1

            if len(finalScores) > 0:
                prediction = finalScores[0]
                (p,d) = prediction
                if correctMapping == p:
                    correctlyLabelledTop1Col = correctlyLabelledTop1Col + 1
                else:
                    pass
                    #print "NOT correct mapping: " + str(correctMapping) + " - " + str(p)
                    #print datasetPrediction.datasetPath
                    #print finalScores
            else:
                pass
                #print "NOT correct mapping: " + str(correctMapping) + " - empty"
                #print datasetPrediction.datasetPath
                #print finalScores



        print " COLUMN LEVEL ANALYSIS: "
        print 'top 1 correctly labelled: ' + str(correctlyLabelledTop1Col)
        print 'top 3 correctly labelled: ' + str(correctlyLabelledTop3Col)
        print 'top X correctly labelled: ' + str(correctlyLabelledTopXCol)
        print 'total: ' + str(totalCol)

        results['top1col']  = correctlyLabelledTop1Col
        results['top3col']  = correctlyLabelledTop3Col
        results['topXcol']  = correctlyLabelledTopXCol
        results['total']    = totalCol


        # --------------------- ROW LEVEL ANALYSIS -----------------------------

        correctlyLabelledTop1Row = 0
        correctlyLabelledTop3Row = 0
        correctlyLabelledTopXRow = 0
        totalRow = 0

        for datasetPrediction in self.datasetsPredictions:
            totalRow = totalRow + 1
            correctMapping =  self.getPropertyName(datasetPrediction.columnMapping[2])

            # calculating from top 3 predictions
            counter = 0
            # [2] because we are interested in only column 2 in the datasets
            finalScores = datasetPrediction.scores['rowResults'][2]
            for prediction in enumerate(finalScores):
                if counter <= 2:
                    (p,d) = prediction[1]
                    if correctMapping == p:
                        correctlyLabelledTop3Row = correctlyLabelledTop3Row + 1
                counter = counter + 1

            # calculating if any predictions
            for prediction in enumerate(finalScores):
                (p,d) = prediction[1]
                if correctMapping == p:
                    correctlyLabelledTopXRow = correctlyLabelledTopXRow + 1
            if len(finalScores) > 0:
                prediction = finalScores[0]
                (p,d) = prediction
                if correctMapping == p:
                    correctlyLabelledTop1Row = correctlyLabelledTop1Row + 1
                else:
                    pass
            #         print "NOT correct mapping: " + str(correctMapping) + " - " + str(p)
            #         print datasetPrediction.datasetPath
            #         print finalScores
            else:
                pass
                #print "NOT correct mapping: " + str(correctMapping) + " - empty"
                #print datasetPrediction.datasetPath
                #print finalScores

        print " ROW LEVEL ANALYSIS: "
        print 'top 1 correctly labelled: ' + str(correctlyLabelledTop1Row)
        print 'top 3 correctly labelled: ' + str(correctlyLabelledTop3Row)
        print 'top X correctly labelled: ' + str(correctlyLabelledTopXRow)
        print 'total: ' + str(totalRow)

        results['top1row']  = correctlyLabelledTop1Row
        results['top3row']  = correctlyLabelledTop3Row
        results['topXrow']  = correctlyLabelledTopXRow

        return results


    def getPropertyName(self, fullProperty):
        return fullProperty[28:]
