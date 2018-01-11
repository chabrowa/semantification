from approach.Semantification import Semantification

from approach.config.paths import *
from approach.config.imports import *

#for fn in os.listdir(datasetsPath):
#    sem = Semantification(fn)
#    sem.getColumnsPredictionsKS()

sem = Semantification('dbpediaTest.csv')

print sem.dataset.subjectColumn.columnValues
