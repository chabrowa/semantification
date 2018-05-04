import commands
import operator

from approach.CellTypeResponse import CellTypeResponse
from approach.config.paths import *

class SubjectColumn(object):

    def __init__(self, columnValues):
	print columnValues	
        print "SUBJECT COLUMN FUN"
	self.columnValues    = columnValues
        self.cellPredictions = self.getCellPredictions()
        self.columnTypes     = self.getMostCommonTypes(self.cellPredictions)

    def getCellPredictions(self):
        predictions = []
        counter = 0
        for index, cell in enumerate(self.columnValues):
            if counter < noRowsToCheck:
		print "WE ARE HERE WE ARE HERE WE ARE HERE"
                predictions.append(self.getCellType(cell))
            counter += 1
        return predictions

    def getCellType(self, cell):
        response = CellTypeResponse(cell, commands.getstatusoutput('curl http://model.dbpedia-spotlight.org/en/annotate  \
          --data-urlencode "text=' + str(cell) + '" \
          --data "confidence=0.05" \
          -H "Accept:text/xml"'))
	print response
        return response

    def getMostCommonTypes(self, predictions):
        predictionsPopularity = {}

        for i, response in enumerate(predictions):
            if response.types != -1:
                types = response.types.split(',')
                for t in types:
                    if t != "":
                        try:
                            (ontology,label) = t.split(":")
                            if ontology == "DBpedia":
                                if t in predictionsPopularity:
                                    predictionsPopularity[t] += 1
                                else:
                                    predictionsPopularity[t] = 1
                        except:
                            pass

        predictionsPopularitySorted = sorted(predictionsPopularity.items(), key=operator.itemgetter(1), reverse=True)

        return predictionsPopularitySorted
