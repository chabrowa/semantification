import commands
import operator

from approach.CellTypeResponse import CellTypeResponse
from approach.config.paths import *

class Column(object):

    def __init__(self, columnId, columnValues):
        self.columnId        = columnId
        self.columnValues   = columnValues
