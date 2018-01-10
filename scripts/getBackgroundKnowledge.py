

from approach.SubjectColumn import SubjectColumn
from approach.BackgroundKnowledge import BackgroundKnowledge

subjectColumn = SubjectColumn(['London','Poland','Potatoes'])
backgroundKnowledge = BackgroundKnowledge('1', subjectColumn.columnTypes, subjectColumn.cellPredictions)


#for index, bag in enumerate(backgroundKnowledge.valuesBags):
    #print bag.values

for index, bag in enumerate(backgroundKnowledge.entityBags):
    print bag.values
