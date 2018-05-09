from scipy import stats
from scipy.spatial import distance
from collections import Counter
import re


from approach.config.paths import *
from approach.config.imports import *

class SimilarityMeasures(object):

    def __init__(self):
        pass

    # The null-hypothesis for the KT test is that the distributions are the same. Thus, the lower your p value the greater the statistical evidence you have to reject the null hypothesis and conclude the distributions are different. The test only really lets you speak of your confidence that the distributions are different, not the same, since the test is designed to find alpha, the probability of Type I error.
    def KSTest(self, bag1, bag2):
        return stats.ks_2samp(bag1, bag2)

    def cosineSimilarity(self, bag1, bag2):
        v1,v2= self.buildVector(bag1, bag2)
        return distance.cosine(v1, v2)

    def euclideanDistance(self, bag1, bag2):
        bag1Border = [bag1[0], bag1[len(bag1)-1]]
        bag2Border = [bag2[0], bag2[len(bag2)-1]]
        return distance.euclidean(bag1Border, bag2Border)

    def euclideanDistanceVector(self, bag1, bag2):
        v1,v2= self.buildVector(bag1, bag2)
        return distance.euclidean(v1, v2)

    def buildVector(self, iterable1, iterable2):
        counter1 = Counter(iterable1)
        counter2= Counter(iterable2)
        all_items = set(counter1.keys()).union( set(counter2.keys()) )
        vector1 = [counter1[k] for k in all_items]
        vector2 = [counter2[k] for k in all_items]
        return vector1, vector2

    def relativeDifference(self, val1, val2):
        try:
            val1 = float(self.getTrim(str(val1)))
            val2 = float(self.getTrim(str(val2)))
            if max(abs(val1), abs(val2)) == 0:
                relDiff = 0
            else:
                relDiff = (abs(val1 - val2))/(max(abs(val1), abs(val2)))

            return relDiff
        except:
            return 1

    def getTrim(self, val):
        trimVal = ''
        for c in val:
            if c.isdigit() or c == '.':
                trimVal = trimVal + c
        return trimVal
