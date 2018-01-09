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

        for filename in os.listdir(self.folder):
            fileCsv = dirName + '/' + filename
            # base = os.path.basename(filename)
            fileNew = os.path.splitext(filename)[0]
            df = pd.read_csv(fileCsv)
            noRows = len(df)
            small = (5*noRows)/100
            medium = (10 * noRows) / 100
            large = (10 * noRows) / 100

            try:
                ###save 5% sample plus variations
                fileSmall = 'smallSample/' + fileNew + '-small.csv'
                df_small = df.sample(small)
                df_small.to_csv(fileSmall)

                df_smallMod = df_small
                df_smallMod[df_smallMod.columns[1]] = df_smallMod[df_smallMod.columns[1]].apply(lambda x: self.fivePerCentMod(x))
                fileSmall = 'smallSample/' + fileNew + '-small-5var.csv'
                df_smallMod.to_csv(fileSmall)

                df_smallMod = df_small
                df_smallMod[df_smallMod.columns[1]] = df_smallMod[df_smallMod.columns[1]].apply(lambda x: self.tenPerCentMod(x))
                fileSmall = 'smallSample/' +fileNew + '-small-10var.csv'
                df_smallMod.to_csv(fileSmall)

                df_smallMod = df_small
                df_smallMod[df_smallMod.columns[1]] = df_smallMod[df_smallMod.columns[1]].apply(lambda x: self.fifteenPerCentMod(x))
                fileSmall = 'smallSample/' +fileNew + '-small-15var.csv'
                df_smallMod.to_csv(fileSmall)

                ###save 10% sample plus variations
                fileMedium = 'mediumSample/' + fileNew + '-medium.csv'
                df_medium = df.sample(medium)
                df_medium.to_csv(fileMedium)

                df_mediumMod = df_medium
                df_mediumMod[df_mediumMod.columns[1]] = df_mediumMod[df_mediumMod.columns[1]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileMedium = 'mediumSample/' + fileNew + '-medium-5var.csv'
                df_mediumMod.to_csv(fileMedium)

                df_mediumMod = df_medium
                df_mediumMod[df_mediumMod.columns[1]] = df_mediumMod[df_mediumMod.columns[1]].apply(
                    lambda x: self.tenPerCentMod(x))
                fileMedium = 'mediumSample/' + fileNew + '-medium-10var.csv'
                df_mediumMod.to_csv(fileMedium)

                df_mediumMod = df_medium
                df_mediumMod[df_mediumMod.columns[1]] = df_mediumMod[df_mediumMod.columns[1]].apply(
                    lambda x: self.fifteenPerCentMod(x))
                fileMedium = 'mediumSample/' + fileNew + '-medium-15var.csv'
                df_mediumMod.to_csv(fileMedium)

                ###save 15% sample plus variations
                fileLarge = 'largeSample/' + fileNew + '-large.csv'
                df_large = df.sample(large)
                df_large.to_csv(fileLarge)

                df_largeMod = df_large
                df_largeMod[df_largeMod.columns[1]] = df_largeMod[df_largeMod.columns[1]].apply(
                    lambda x: self.fivePerCentMod(x))
                fileLarge = 'largeSample/' + fileNew + '-large-5var.csv'
                df_largeMod.to_csv(fileLarge)

                df_largeMod = df_large
                df_largeMod[df_largeMod.columns[1]] = df_largeMod[df_largeMod.columns[1]].apply(
                    lambda x: self.tenPerCentMod(x))
                fileLarge = 'largeSample/' + fileNew + '-large-10var.csv'
                df_largeMod.to_csv(fileLarge)

                df_largeMod = df_large
                df_largeMod[df_largeMod.columns[1]] = df_largeMod[df_largeMod.columns[1]].apply(
                    lambda x: self.fifteenPerCentMod(x))
                fileLarge = 'largeSample/' + fileNew + '-large-15var.csv'
                df_largeMod.to_csv(fileLarge)

            except ValueError:
                pass



    def fivePerCentMod(self, no):
        print type(no)

        upMod = no + ((no * 5)/100)
        downMod = no - ((no * 5)/100)
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