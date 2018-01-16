from approach.config.paths import *
from approach.config.imports import *

from evaluation.Experiment import Experiment

class Evaluation(object):

    def __init__(self, benchmarkPath):
        self.benchmarkPath       = benchmarkPath
        self.experiments         = self.getExperiments()


    def getExperiments(self):
        experiments = []
        sizes = ['small', 'medium', 'large']
        deviations = [0, 5, 10, 15]

        for s in sizes:
            for d in deviations:
                expPath = evaluationPath + s + 'Sample/' + s + str(s) + "/"
                experiments.append(Experiment(3, s, d, expPath))
        return experiments

    def getScores(self):
        pass
