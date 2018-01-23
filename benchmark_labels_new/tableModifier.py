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

        dirName = os.path.abspath(self.folder)

        directories = ['smallSample/small', 'smallSample/small5', 'smallSample/small10', 'smallSample/small15', 'mediumSample/medium', 'mediumSample/medium5', 'mediumSample/medium10', 'mediumSample/medium15', 'largeSample/large', 'largeSample/large5', 'largeSample/large10', 'largeSample/large15']

        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)

        for filename in os.listdir(self.folder):
            fileCsv = dirName + '/' + filename
            # base = os.path.basename(filename)
            fileNew = os.path.splitext(filename)[0]
            df = pd.read_csv(fileCsv)
            noRows = len(df)
            small = (5*noRows)/100
            medium = (10 * noRows) / 100
            large = (15 * noRows) / 100

            try:
                ###save 5% sample plus variations
                fileSmall = 'smallSample/small/' + fileNew + '-small.csv'
                df_small = df.sample(small)
                if df_small.shape[0] > 1:
                    df_small.to_csv(fileSmall, index=False)

                df_smallMod = df_small
                df_smallMod[df_smallMod.columns[1]] = df_smallMod[df_smallMod.columns[1]].apply(lambda x: self.fivePerCentMod(x))
                fileSmall = 'smallSample/small5/' + fileNew + '-small-5var.csv'
                if df_smallMod.shape[0] > 1:
                    df_smallMod.to_csv(fileSmall, index=False)

                df_smallMod = df_small
                df_smallMod[df_smallMod.columns[1]] = df_smallMod[df_smallMod.columns[1]].apply(lambda x: self.tenPerCentMod(x))
                fileSmall = 'smallSample/small10/' +fileNew + '-small-10var.csv'
                if df_smallMod.shape[0] > 1:
                    df_smallMod.to_csv(fileSmall, index=False)

                df_smallMod = df_small
                df_smallMod[df_smallMod.columns[1]] = df_smallMod[df_smallMod.columns[1]].apply(lambda x: self.fifteenPerCentMod(x))
                fileSmall = 'smallSample/small15/' +fileNew + '-small-15var.csv'
                if df_smallMod.shape[0] > 1:
                    df_smallMod.to_csv(fileSmall, index=False)

                ###save 10% sample plus variations
                fileMedium = 'mediumSample/medium/' + fileNew + '-medium.csv'
                df_medium = df.sample(medium)
                if df_medium.shape[0] > 1:
                    df_medium.to_csv(fileMedium, index=False)

                df_mediumMod = df_medium
                df_mediumMod[df_mediumMod.columns[1]] = df_mediumMod[df_mediumMod.columns[1]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileMedium = 'mediumSample/medium5/' + fileNew + '-medium-5var.csv'
                if df_mediumMod.shape[0] > 1:
                    df_mediumMod.to_csv(fileMedium, index=False)

                df_mediumMod = df_medium
                df_mediumMod[df_mediumMod.columns[1]] = df_mediumMod[df_mediumMod.columns[1]].apply(
                    lambda x: self.tenPerCentMod(x))
                fileMedium = 'mediumSample/medium10/' + fileNew + '-medium-10var.csv'
                if df_mediumMod.shape[0] > 1:
                    df_mediumMod.to_csv(fileMedium, index=False)

                df_mediumMod = df_medium
                df_mediumMod[df_mediumMod.columns[1]] = df_mediumMod[df_mediumMod.columns[1]].apply(
                    lambda x: self.fifteenPerCentMod(x))
                fileMedium = 'mediumSample/medium15/' + fileNew + '-medium-15var.csv'
                if df_mediumMod.shape[0] > 1:
                    df_mediumMod.to_csv(fileMedium, index=False)

                ###save 15% sample plus variations
                fileLarge = 'largeSample/large/' + fileNew + '-large.csv'
                df_large = df.sample(large)
                if df_large.shape[0] > 1:
                    df_large.to_csv(fileLarge, index=False)

                df_largeMod = df_large
                df_largeMod[df_largeMod.columns[1]] = df_largeMod[df_largeMod.columns[1]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileLarge = 'largeSample/large5/' + fileNew + '-large-5var.csv'
                if df_largeMod.shape[0] > 1:
                    df_largeMod.to_csv(fileLarge, index=False)

                df_largeMod = df_large
                df_largeMod[df_largeMod.columns[1]] = df_largeMod[df_largeMod.columns[1]].apply(
                    lambda x: self.tenPerCentMod(x))
                fileLarge = 'largeSample/large10/' + fileNew + '-large-10var.csv'
                if df_largeMod.shape[0] > 1:
                    df_largeMod.to_csv(fileLarge, index=False)

                df_largeMod = df_large
                df_largeMod[df_largeMod.columns[1]] = df_largeMod[df_largeMod.columns[1]].apply(
                    lambda x: self.fifteenPerCentMod(x))
                fileLarge = 'largeSample/large15/' + fileNew + '-large-15var.csv'
                if df_largeMod.shape[0] > 1:
                    df_largeMod.to_csv(fileLarge, index=False)

            except ValueError:
                pass



    def fivePerCentMod(self, no):
        # print type(no)
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
        no = int(no)
        upMod = no + ((no * 5) / 100)
        downMod = no - ((no * 5) / 100)
        modRange = random.randint(downMod, upMod)

        return modRange

    def tenPerCentMod(self, no):
        no = int(no)
        upMod = no + ((no * 10) / 100)
        downMod = no - ((no * 10) / 100)
        modRange = random.randint(downMod, upMod)
        return modRange

    def fifteenPerCentMod(self, no):
        no = int(no)
        upMod = no + ((no * 15) / 100)
        downMod = no - ((no * 15) / 100)
        modRange = random.randint(downMod, upMod)
        return modRange


def main():
    folderName = sys.argv[1]
    # file_output = sys.argv[2]
    tableModifier(folderName)


if __name__ == "__main__":
    main()