import pandas as pd
import os
from os.path import isfile, join

from approach.SubjectColumn import SubjectColumn
from approach.config.paths import *

class Dataset(object):

    def __init__(self, datasetId):
        self.datasetId       = datasetId
        self.subjectColumnId = self.getSubjectColumnId()
        self.subjectColumn   = self.getSubjectColumn()

    def getSubjectColumnId(self):
        with open(subjectFile) as f:
            content = f.readlines()

        for line in content:
            (fileDatasetId, subjectColumnIndex) = line.split(",")
            if fileDatasetId == self.datasetId:
                print subjectColumnIndex
                return subjectColumnIndex
        return -100

    def getSubjectColumn(self):
        subjectColumnValues = []
        df = pd.read_csv(os.path.join(datasetsPath, self.datasetId))
        if int(self.subjectColumnId) != -1:
            for index, row in df.iterrows():
                subjectColumnValues.append(row[int(self.subjectColumnId)])

            return SubjectColumn(subjectColumnValues)
        else:
            return -1
