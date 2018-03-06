from approach.Semantification import Semantification

from approach.config.paths import *
from approach.config.imports import *


def checkDataset(dataset):
    #print dataset.size
    if dataset.size > 2:
        return True
    else:
        return False

counter = 1
for fn in os.listdir(datasetsPath):
    #check if the table can be used
    dataset = pd.read_csv(os.path.join(datasetsPath, fn))
    if checkDataset(dataset):
        print list(dataset.columns.values)
        sem = Semantification(fn)
        #sem.getColumnsPredictionsKS()
        counter = counter + 1

#print "counter:" + str(counter)
#sem = Semantification('dbpediaTest.csv')
#print sem.dataset.subjectColumn.columnValues
