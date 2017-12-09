
from approach.SimilarityMeasures import SimilarityMeasures

sm = SimilarityMeasures()
x = [1, 2, 3, 4, 5]
y = [1,3,5]

a = [1,2,3]
b = [1,4,6]

print "KS test; return 2 valuesL statistic (float) KS statistic AND pvalue (float) two-tailed p-value"
print sm.KSTest(x,y)
print sm.KSTest(a,b)

print "Euclidean Distance"
print sm.euclideanDistance(x,y)
print sm.euclideanDistance(a,b)

print "Euclidean Distance Vector"
print sm.euclideanDistanceVector(x,y)
print sm.euclideanDistanceVector(a,b)

print "Cosine Similarity"
print sm.cosineSimilarity(x,y)
print sm.cosineSimilarity(a,b)
