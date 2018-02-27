from approach.config.paths import *
from approach.config.imports import *

from evaluationWithUri.DatasetPrediction import DatasetPrediction

class Experiment(object):

    def __init__(self, size, percentageDeviation, dataPath):
        self.size                = size
        self.dataPath            = dataPath
        #self.datasetsPredictions = self.getDatasetPredictions()
        self.datasetsPredictions = self.getNotWorkingDatasetPredictions()
        self.percentageDeviation = percentageDeviation
        self.score               = self.getScore()


    def getNotWorkingDatasetPredictions(self):
        datasetPredictions = []
        count = 0

        notWorkinDatasets = ['dbo_squadNumber-301-large.csv',
                            'dbo_squadNumber-307-large.csv',
                            'dbo_numberOfEpisodes-222-large.csv',
                            'dbo_populationTotal-346-large.csv',
                            'dbo_squadNumber-306-large.csv',
                            'dbo_numberOfEpisodes-229-large.csv',
                            'dbo_squadNumber-303-large.csv',
                            'dbo_populationTotal-348-large.csv',
                            'dbo_areaWater-180-large.csv',
                            'dbo_areaTotal-290-large.csv',
                            'dbo_squadNumber-305-large.csv',
                            'dbo_numberOfGoals-326-large.csv',
                            'dbo_areaLand-243-large.csv',
                            'dbo_areaLand-249-large.csv',
                            'dbo_squadNumber-302-large.csv',
                            'dbo_capacity-389-large.csv',
                            'dbo_numberOfGoals-321-large.csv',
                            'dbo_runtime-256-large.csv',
                            'dbo_squadNumber-310-large.csv',
                            'dbo_squadNumber-304-large.csv']
        sample = ['dbo_numberOfSeasons-23-large.csv',
        'dbo_populationTotal-347-large.csv',
        'dbo_areaLand-247-large.csv',
        'dbo_gross-122-large.csv',
        'dbo_oclc-217-large.csv',
        'dbo_gross-125-large.csv',
        'dbo_budget-357-large.csv',
        'dbo_routeNumber-2-large.csv',
        'dbo_areaWater-174-large.csv',
        'dbo_oclc-216-large.csv',
        'dbo_routeNumber-4-large.csv',
        'dbo_areaCode-194-large.csv',
        'dbo_squadNumber-303-large.csv',
        'dbo_populationTotal-348-large.csv',
        'dbo_squadNumber-308-large.csv',
        'dbo_areaLand-243-large.csv',
        'dbo_areaLand-244-large.csv',
        'dbo_budget-358-large.csv',
        'dbo_areaLand-250-large.csv',
        'dbo_numberOfEpisodes-226-large.csv',
        'dbo_numberOfSeasons-26-large.csv',
        'dbo_minimumElevation-167-large.csv',
        'dbo_maximumElevation-413-large.csv',
        'dbo_runwayLength-148-large.csv']

        sample2 = ['dbo_draftYear-339-large.csv',
        'dbo_serviceStartYear-425-large.csv',
        'dbo_yearOfConstruction-396-large.csv',
        'dbo_activeYearsEndYear-56-large.csv',
        'dbo_serviceEndYear-37-large.csv',
        'dbo_openingYear-368-large.csv',
        'dbo_deathYear-208-large.csv',
        'dbo_openingYear-362-large.csv',
        'dbo_formationYear-137-large.csv',
        'dbo_serviceStartYear-426-large.csv',
        'dbo_foundingYear-298-large.csv',
        'dbo_yearOfConstruction-391-large.csv',
        'dbo_deathYear-204-large.csv',
        'dbo_serviceEndYear-36-large.csv',
        'dbo_yearOfConstruction-400-large.csv',
        'dbo_foundingYear-295-large.csv',
        'dbo_deathYear-209-large.csv',
        'dbo_yearOfConstruction-394-large.csv',
        'dbo_serviceEndYear-33-large.csv',
        'dbo_populationDensity-401-large.csv',
        'dbo_draftYear-333-large.csv',
        'dbo_serviceStartYear-422-large.csv',
        'dbo_deathYear-201-large.csv',
        'dbo_formationYear-138-large.csv',
        'dbo_foundingYear-296-large.csv',
        'dbo_year-445-large.csv',
        'dbo_yearOfConstruction-399-large.csv',
        'dbo_formationYear-135-large.csv',
        'dbo_activeYearsEndYear-59-large.csv',
        'dbo_serviceEndYear-35-large.csv',
        'dbo_draftYear-335-large.csv',
        'dbo_activeYearsStartYear-160-large.csv',
        'dbo_deathYear-207-large.csv',
        'dbo_draftYear-338-large.csv',
        'dbo_serviceStartYear-424-large.csv',
        'dbo_activeYearsStartYear-152-large.csv',
        'dbo_year-449-large.csv',
        'dbo_yearOfConstruction-398-large.csv',
        'dbo_foundingYear-297-large.csv',
        'dbo_openingYear-367-large.csv',
        'dbo_activeYearsEndYear-60-large.csv',
        'dbo_activeYearsEndYear-55-large.csv',
        'dbo_activeYearsStartYear-154-large.csv',
        'dbo_serviceEndYear-39-large.csv',
        'dbo_activeYearsStartYear-159-large.csv',
        'dbo_activeYearsEndYear-58-large.csv',
        'dbo_foundingYear-291-large.csv',
        'dbo_openingYear-361-large.csv']

        sample3 = ['dbo_populationDensity-408-medium.csv']

        for fn in os.listdir(self.dataPath):
            #if fn in sample3:
            datasetPath = os.path.join(self.dataPath, fn)
            dataset = DatasetPrediction(datasetPath)
            if dataset.scores != -1:
                datasetPredictions.append(dataset)
            count = count + 1
            print count
        print "all datasets: " + str(count)

        return datasetPredictions

    def getDatasetPredictions(self):
        datasetPredictions = []
        count = 1
        for fn in os.listdir(self.dataPath):
            #print str(count) + ":  " + str(fn)
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
            correctMapping =  self.getPropertyName(datasetPrediction.columnMapping[1])

            # calculating from top 3 predictions
            counter = 0
            for prediction in enumerate(datasetPrediction.scores['finalResults'][1]):
                if counter <= 2:
                    (p,d) = prediction[1]
                    if correctMapping == p:
                        correctlyLabelledTop3 = correctlyLabelledTop3 + 1
                counter = counter + 1

            # calculating if any predictions
            for prediction in enumerate(datasetPrediction.scores['finalResults'][1]):
                (p,d) = prediction[1]
                if correctMapping == p:
                    correctlyLabelledTopX = correctlyLabelledTopX + 1
            #print datasetPrediction.datasetPath
            #print datasetPrediction.scores['finalResults'][1]

            # calculating from top 1 predictions
            #print datasetPrediction.scores['finalResults'][1]
            prediction = datasetPrediction.scores['finalResults'][1][0]
            (p,d) = prediction
            if correctMapping == p:
                #print "correct mapping: " + str(correctMapping) + " - " + str(p)
                correctlyLabelledTop1 = correctlyLabelledTop1 + 1
            else:
                print "NOT correct mapping: " + str(correctMapping) + " - " + str(p)
                print datasetPrediction.datasetPath
                print datasetPrediction.scores['finalResults'][1]



        print 'top 1 correctly labelled: ' + str(correctlyLabelledTop1)
        print 'top 3 correctly labelled: ' + str(correctlyLabelledTop3)
        print 'top X correctly labelled: ' + str(correctlyLabelledTopX)
        print 'total: ' + str(total)

        return 0

    def getPropertyName(self, fullProperty):
        return fullProperty[28:]
