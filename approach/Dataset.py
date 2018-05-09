import pandas as pd
import os
from os.path import isfile, join

from approach.SubjectColumn import SubjectColumn
from approach.Column import Column
from approach.config.paths import *
from approach.config.imports import *

class Dataset(object):

    def __init__(self, datasetId, subjectColumnId, numericalColumnsIds):
        self.datasetId              = datasetId
        self.df                     = pd.read_csv(datasetId)
        self.subjectColumnId        = subjectColumnId
        self.subjectColumn          = self.getSubjectColumn()
        if numericalColumnsIds == None:
            self.numericalColumnsIds    = self.getNumericalColumnsIds()
        else:
            self.numericalColumnsIds    = numericalColumnsIds
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

    def getSubjectColumn(self):
        subjectColumnValues = []
        if int(self.subjectColumnId) != -1:
            for index, row in self.df.iterrows():
                subjectColumnValues.append(row[int(self.subjectColumnId)])

            return SubjectColumn(subjectColumnValues)
        else:
            return -1

    def getNumericalColumnsIds(self):
        numericalColumnsIds = []
        for index, column in enumerate(self.df):
            column = (self.df[column])
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
