from scipy import stats
from scipy.spatial import distance
from collections import Counter

from approach.config.paths import *
from approach.config.imports import *

class SimilarityMeasures(object):

    def __init__(self):
        pass

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
