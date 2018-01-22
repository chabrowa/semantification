from approach.config.paths import *
from approach.config.imports import *

from evaluationWithUri.Experiment import Experiment

class Evaluation(object):

    def __init__(self,sizes,deviations):
        self.sizes       = sizes
        self.deviations  = deviations
        self.experiments = self.getExperiments()

    def getExperiments(self):
        experiments = []

        for s in self.sizes:
            for d in self.deviations:
                #expPath = evaluationPath + s + 'Sample/' + s + str(d) + "/"
                expPath = evaluationPath + s + 'Sample/' + s + str(d) + "/"
                experiments.append(Experiment(s, d, expPath))
        return experiments

    def getScores(self):
        pass
