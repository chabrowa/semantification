from approach.config.paths import *
from approach.config.imports import *

from evaluationSubmission.Experiment import Experiment

class Evaluation(object):

    def __init__(self,sizes,deviations):
        self.sizes       = sizes
        self.deviations  = deviations
        self.experiments = self.getExperiments()

    def getExperiments(self):
        experiments = []

        for s in self.sizes:
            for d in self.deviations:
                print "Size: " + str(s) + " Deviation: " + str(d)
                #expPath = evaluationPath + s + 'Sample/' + s + str(d) + "/"
                expPath = evaluationPath + s + 'Sample/' + s + str(d) + "/"
                experiments.append(Experiment(s, d, expPath))
        return experiments

    def getResults(self):
        for e in self.experiments:
            pass
