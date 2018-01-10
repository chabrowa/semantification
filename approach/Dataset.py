import pandas as pd
import os
from os.path import isfile, join

from approach.SubjectColumn import SubjectColumn
from approach.Column import Column
from approach.config.paths import *
from approach.config.imports import *

class Dataset(object):

    # def __init__(self, datasetId):
    #     self.datasetId              = datasetId
    #     self.df                     = pd.read_csv(os.path.join(datasetsPath, datasetId))
    #     self.subjectColumnId        = self.getSubjectColumnId()
    #     self.subjectColumn          = self.getSubjectColumn()
    #     self.numericalColumnsIds    = self.getNumericalColumnsIds()
    #     self.columnsWithMappingsIds = self.getColumnsWithMappingsIds()
    #     self.columnsWithMappings    = self.getColumnsWithMappings()
    #     self.columns                = self.getColumns()

    def __init__(self, datasetId):
        self.datasetId              = datasetId
        self.df                     = pd.read_csv(os.path.join(datasetsPath, datasetId))
        self.subjectColumnId        = 0
        self.subjectColumn          = self.getSubjectColumn()
        self.columnsWithMappingsIds = [1]
        self.numericalColumnsIds    = [1]
        self.columns                = self.getColumns()

    def getColumns(self):
        columns = []
        for index, column in enumerate(self.df):
            column = (self.df[column])
            columns.append(Column(index, column))
        return columns

    def getColumnValues(self, columnId):
        return self.columns[columnId].columnValues

    def getCellValue(self, columnId, subjectCellValue):
        if int(self.subjectColumnId) != -1:
            for index, row in self.df.iterrows():
                if row[int(self.subjectColumnId)] == subjectCellValue:
                    cell = row[columnId]
        return cell

    def getSubjectColumnId(self):
        with open(subjectFile) as f:
            content = f.readlines()

        for line in content:
            (fileDatasetId, subjectColumnIndex) = line.split(",")
            if fileDatasetId == self.datasetId:
                #print subjectColumnIndex
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

    def getNumericalColumnsIds(self):
        numericalColumnsIds = []
        df = pd.read_csv(datasetsPath + self.datasetId)
        for index, column in enumerate(df):
            column = (df[column])
            if self.columnHasNumbers(column):
                if index != self.subjectColumnId:
                    numericalColumnsIds.append(index)
        return numericalColumnsIds

    def is_num_in_str(self, inputString):
        return bool(re.search(r'\d', str(inputString)))

    def columnHasNumbers(self, column):
        counter = 0
        noValues = len(column)
        for c in column:
            if self.is_num_in_str(c):
                counter = counter + 1
        score = float(counter)/float(noValues)
        if score>=0.5:
            return True
        return False

    def getColumnsWithMappingsIds(self):
        columnsWithMappingsIds = []
        mappingFile = os.path.join(mappingsPath, self.datasetId)
        df = pd.read_csv(mappingFile,  header=None)
        for index, row in df.iterrows():
            columnsWithMappingsIds.append(int(row[3]))
        return columnsWithMappingsIds

    def getColumnsWithMappings(self):
        columnsWithMappings = {}
        mappingFile = os.path.join(mappingsPath, self.datasetId)
        df = pd.read_csv(mappingFile,  header=None)
        for index, row in df.iterrows():
            columnsWithMappings[int(row[3])] = row[0]
        return columnsWithMappings
