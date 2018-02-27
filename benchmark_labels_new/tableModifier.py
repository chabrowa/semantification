#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import pandas as pd
import random
import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import numpy as np
import csv


class tableModifier(object):

    def __init__(self, folder):
        self.folder = folder
        # self.fileOut = fileOut
        self.fileIterator()


    def fileIterator(self):
        self.dictFileLength = {}
        dirName = os.path.abspath(self.folder)

        directories = ['verySmallSample/smallest/', 'verySmallSample/smallest5/', 'verySmallSample/smallest10/', 'verySmallSample/smallest15/',
                       'smallSample/small', 'smallSample/small5', 'smallSample/small10', 'smallSample/small15',
                       'mediumSample/medium', 'mediumSample/medium5', 'mediumSample/medium10', 'mediumSample/medium15',
                       'largeSample/large', 'largeSample/large5', 'largeSample/large10', 'largeSample/large15']

        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

        for filename in os.listdir(self.folder):
            fileCsv = dirName + '/' + filename
            # base = os.path.basename(filename)
            fileNew = os.path.splitext(filename)[0]
            df = pd.read_csv(fileCsv)
            noRows = len(df)
            smallest = int(noRows / 100)
            small = int((5 * noRows) / 100)
            medium = int((10 * noRows) / 100)
            large = int((15 * noRows) / 100)
            filePrint = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]

            try:

                ###save 1% sample plus variations
                fileVerySmall = 'verySmallSample/smallest/' + fileNew + '-smallest.csv'
                df_smallest = df.sample(smallest)
                if df_smallest.shape[0] > 1:
                    filePrint[12] = True

                ###save 5% sample plus variations
                fileSmall = 'smallSample/small/' + fileNew + '-small.csv'
                df_small = df.sample(small)
                if df_small.shape[0] > 1:
                    filePrint[0] = True

                ###save 10% sample plus variations
                fileMedium = 'mediumSample/medium/' + fileNew + '-medium.csv'
                df_medium = df.sample(medium)
                if df_medium.shape[0] > 1:
                    filePrint[1] = True

                ###save 15% sample plus variations
                fileLarge = 'largeSample/large/' + fileNew + '-large.csv'
                df_large = df.sample(large)
                if df_large.shape[0] > 1:
                    filePrint[2] = True

                df_smallestMod5 = df_smallest
                df_smallestMod5[df_smallestMod5.columns[2]] = df_smallestMod5[df_smallestMod5.columns[2]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileSmallest_mod5 = 'verySmallSample/smallest5/' + fileNew + '-smallest.csv'
                if df_smallestMod5.shape[0] > 1:
                    filePrint[13] = True

                df_smallestMod10 = df_smallest
                df_smallestMod10[df_smallestMod10.columns[2]] = df_smallestMod10[df_smallestMod5.columns[2]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileSmallest_mod10 = 'verySmallSample/smallest10/' + fileNew + '-smallest.csv'
                if df_smallestMod10.shape[0] > 1:
                    filePrint[14] = True

                df_smallestMod15 = df_smallest
                df_smallestMod15[df_smallestMod15.columns[2]] = df_smallestMod15[df_smallestMod15.columns[2]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileSmallest_mod15 = 'verySmallSample/smallest15/' + fileNew + '-smallest.csv'
                if df_smallestMod15.shape[0] > 1:
                    filePrint[15] = True

                df_smallMod5 = df_small
                df_smallMod5[df_smallMod5.columns[2]] = df_smallMod5[df_smallMod5.columns[2]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileSmall_mod5 = 'smallSample/small5/' + fileNew + '-small-5var.csv'
                if df_smallMod5.shape[0] > 1:
                    filePrint[3] = True

                df_smallMod10 = df_small
                df_smallMod10[df_smallMod10.columns[2]] = df_smallMod10[df_smallMod10.columns[2]].apply(
                    lambda x: self.tenPerCentMod(x))
                fileSmall_mod10 = 'smallSample/small10/' + fileNew + '-small-10var.csv'
                if df_smallMod10.shape[0] > 1:
                    filePrint[4] = True

                df_smallMod15 = df_small
                df_smallMod15[df_smallMod15.columns[2]] = df_smallMod15[df_smallMod15.columns[2]].apply(
                    lambda x: self.fifteenPerCentMod(x))
                fileSmall_mod15 = 'smallSample/small15/' + fileNew + '-small-15var.csv'
                if df_smallMod15.shape[0] > 1:
                    filePrint[5] = True

                df_mediumMod5 = df_medium
                df_mediumMod5[df_mediumMod5.columns[2]] = df_mediumMod5[df_mediumMod5.columns[2]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileMedium_mod5 = 'mediumSample/medium5/' + fileNew + '-medium-5var.csv'
                if df_mediumMod5.shape[0] > 1:
                    filePrint[6] = True

                df_mediumMod10 = df_medium
                df_mediumMod10[df_mediumMod10.columns[2]] = df_mediumMod10[df_mediumMod10.columns[2]].apply(
                    lambda x: self.tenPerCentMod(x))
                fileMedium_mod10 = 'mediumSample/medium10/' + fileNew + '-medium-10var.csv'
                if df_mediumMod10.shape[0] > 1:
                    filePrint[7] = True

                df_mediumMod15 = df_medium
                df_mediumMod15[df_mediumMod15.columns[2]] = df_mediumMod15[df_mediumMod15.columns[2]].apply(
                    lambda x: self.fifteenPerCentMod(x))
                fileMedium_mod15 = 'mediumSample/medium15/' + fileNew + '-medium-15var.csv'
                if df_mediumMod15.shape[0] > 1:
                    filePrint[8] = True

                df_largeMod5 = df_large
                df_largeMod5[df_largeMod5.columns[2]] = df_largeMod5[df_largeMod5.columns[2]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileLarge_mod5 = 'largeSample/large5/' + fileNew + '-large-5var.csv'
                if df_largeMod5.shape[0] > 1:
                    filePrint[9] = True

                df_largeMod10 = df_large
                df_largeMod10[df_largeMod10.columns[2]] = df_largeMod10[df_largeMod10.columns[2]].apply(
                    lambda x: self.tenPerCentMod(x))
                fileLarge_mod10 = 'largeSample/large10/' + fileNew + '-large-10var.csv'
                if df_largeMod10.shape[0] > 1:
                    filePrint[10] = True

                df_largeMod15 = df_large
                df_largeMod15[df_largeMod15.columns[2]] = df_largeMod15[df_largeMod15.columns[2]].apply(
                    lambda x: self.fifteenPerCentMod(x))
                fileLarge_mod15 = 'largeSample/large15/' + fileNew + '-large-15var.csv'
                if df_largeMod15.shape[0] > 1:
                    filePrint[11] = True

                if all(x is True for x in filePrint):
                    df_smallest.to_csv(fileVerySmall, index=False)
                    self.dictFileLength[fileVerySmall] = df_smallest.shape[0]
                    df_small.to_csv(fileSmall, index=False)
                    self.dictFileLength[fileSmall] = df_small.shape[0]
                    df_medium.to_csv(fileMedium, index=False)
                    self.dictFileLength[fileMedium] = df_medium.shape[0]
                    df_large.to_csv(fileLarge, index=False)
                    self.dictFileLength[fileLarge] = df_large.shape[0]

                    df_smallestMod5.to_csv(fileSmallest_mod5, index=False)
                    self.dictFileLength[fileSmallest_mod5] = df_smallestMod5.shape[0]
                    df_smallestMod10.to_csv(fileSmallest_mod10, index=False)
                    self.dictFileLength[fileSmallest_mod10] = df_smallestMod10.shape[0]
                    df_smallestMod15.to_csv(fileSmallest_mod15, index=False)
                    self.dictFileLength[fileSmallest_mod15] = df_smallestMod15.shape[0]

                    df_smallMod5.to_csv(fileSmall_mod5, index=False)
                    self.dictFileLength[fileSmall_mod5] = df_smallMod5.shape[0]
                    df_smallMod10.to_csv(fileSmall_mod10, index=False)
                    self.dictFileLength[fileSmall_mod10] = df_smallMod10.shape[0]
                    df_smallMod15.to_csv(fileSmall_mod15, index=False)
                    self.dictFileLength[fileSmall_mod15] = df_smallMod15.shape[0]

                    df_mediumMod5.to_csv(fileMedium_mod5, index=False)
                    self.dictFileLength[fileMedium_mod5] = df_mediumMod5.shape[0]
                    df_mediumMod10.to_csv(fileMedium_mod10, index=False)
                    self.dictFileLength[fileMedium_mod10] = df_mediumMod10.shape[0]
                    df_mediumMod15.to_csv(fileMedium_mod15, index=False)
                    self.dictFileLength[fileMedium_mod15] = df_mediumMod15.shape[0]

                    df_largeMod5.to_csv(fileLarge_mod5, index=False)
                    self.dictFileLength[fileLarge_mod5] = df_largeMod5.shape[0]
                    df_largeMod10.to_csv(fileLarge_mod10, index=False)
                    self.dictFileLength[fileLarge_mod10] = df_largeMod10.shape[0]
                    df_largeMod15.to_csv(fileLarge_mod15, index=False)
                    self.dictFileLength[fileLarge_mod15] = df_largeMod15.shape[0]


                    fileLengthDf = pd.DataFrame.from_dict(self.dictFileLength, orient='index')
                    fileNameLength = 'fileLengthData.csv'
                    fileLengthDf.to_csv(fileNameLength, mode='w')

            except ValueError:
                pass

    def fivePerCentMod(self, no):
        # try:
        #     upMod = no + ((no * 5)/100)
        #     downMod = no - ((no * 5)/100)
        #     modRange = random.randint(downMod, upMod)
        # except TypeError:
        #     try:
        #         no = ''.join(e for e in no if e.isalnum())
        #         no = int(no)
        #         upMod = no + ((no * 5) / 100)
        #         downMod = no - ((no * 5) / 100)
        #         modRange = random.randint(downMod, upMod)
        #     except:
        #         modRange = 0
        if type(no) == float:
            upMod = no + ((no * 5) / 100)
            downMod = no - ((no * 5) / 100)
            modRange = random.uniform(downMod, upMod)
        elif type(no) == int:
            upMod = no + ((no * 5) / 100)
            downMod = no - ((no * 5) / 100)
            modRange = random.randint(int(downMod), int(upMod))
        else:

            try:
                no = int(no)

                upMod = no + ((no * 5) / 100)
                downMod = no - ((no * 5) / 100)
                modRange = random.randint(int(downMod), int(upMod))
            except:
                no = float(no)

                upMod = no + ((no * 5) / 100)
                downMod = no - ((no * 5) / 100)
                modRange = random.uniform(downMod, upMod)

        return modRange

    def tenPerCentMod(self, no):
        if type(no) == float:
            upMod = no + ((no * 10) / 100)
            downMod = no - ((no * 10) / 100)
            modRange = random.uniform(downMod, upMod)
        elif type(no) == int:
            upMod = no + ((no * 10) / 100)
            downMod = no - ((no * 10) / 100)
            modRange = random.randint(int(downMod), int(upMod))
        else:

            try:
                no = int(no)

                upMod = no + ((no * 10) / 100)
                downMod = no - ((no * 10) / 100)
                modRange = random.randint(int(downMod), int(upMod))
            except:
                no = float(no)

                upMod = no + ((no * 10) / 100)
                downMod = no - ((no * 10) / 100)
                modRange = random.uniform(downMod, upMod)

        return modRange

    def fifteenPerCentMod(self, no):
        if type(no) == float:
            upMod = no + ((no * 15) / 100)
            downMod = no - ((no * 15) / 100)
            modRange = random.uniform(downMod, upMod)
        elif type(no) == int:
            upMod = no + ((no * 15) / 100)
            downMod = no - ((no * 15) / 100)
            modRange = random.randint(int(downMod), int(upMod))
        else:

            try:
                no = int(no)

                upMod = no + ((no * 15) / 100)
                downMod = no - ((no * 15) / 100)
                modRange = random.randint(int(downMod), int(upMod))
            except:
                no = float(no)

                upMod = no + ((no * 15) / 100)
                downMod = no - ((no * 15) / 100)
                modRange = random.uniform(downMod, upMod)

        return modRange


def main():
    folderName = sys.argv[1]
    # file_output = sys.argv[2]
    tableModifier(folderName)


if __name__ == "__main__":
    main()
