from approach.Dataset import Dataset

#dataset = Dataset('10786782_0_7941448888047609465.csv')
dataset = Dataset('96960685_0_6886906070865701391.csv')
print "subject columns is " + str(dataset.subjectColumnId)
print "numerical column are [2] "
print dataset.numericalColumnsIds
print dataset.columnsWithMappingsIds


dataset = Dataset('10786782_0_7941448888047609465.csv')
print "subject columns is " + str(dataset.subjectColumnId)
print "numerical column is "
print dataset.numericalColumnsIds
print dataset.columnsWithMappingsIds


dataset = Dataset('52340077_0_7623033473986759010.csv')
print "subject columns is " + str(dataset.subjectColumnId)
print "numerical column is "
print dataset.numericalColumnsIds
print dataset.columnsWithMappingsIds
