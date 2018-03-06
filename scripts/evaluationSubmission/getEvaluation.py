from evaluationSubmission.Evaluation import Evaluation

from approach.config.paths import *
from approach.config.imports import *


sizes = ['verySmall', 'small', 'medium', 'large']
deviations = [0, 5, 10, 15]
e = Evaluation(sizes, deviations)
