from approach.Dataset import Dataset
from approach.config.paths import *
from approach.config.imports import *

for fn in os.listdir(datasetsPath):
    print "______________________________________________"
    print fn
    dataset = Dataset(fn)
