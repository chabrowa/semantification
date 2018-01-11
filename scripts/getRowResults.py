from approach.Semantification import Semantification

from approach.config.paths import *
from approach.config.imports import *

#for fn in os.listdir(datasetsPath):
#    sem = Semantification(fn)
#    sem.getRowPredictions()

sem = Semantification('56834172_0_5710924050177414995.csv')
