
from approach.config.paths import *
from approach.config.imports import *

import datetime


with open("/Users/emiliakacprzak/Code/papers/semantification/times.log", 'r') as myfile:
    counter = 0
    totalFiles = 0
    toCheck = False

    #totalTime = datetime.time()
    for line in myfile:
        if counter == 5:
            #print "----------------------------------"
            counter = 0
        if counter < 5:
            if counter == 0:
                if "largeSample" in line or "mediumSample" in line or "smallSample" in line or "verySmallSample" in line:
                    toCheck = True
                    #print line
                    totalFiles += 1
            if toCheck and counter == 4:
                #lineArray = line.split(' ')
                position = line.find('0:00:')
                compTime = line[position:position+7]
                print compTime
                

                try:
                    finalTime = datetime.strptime(compTime,'%H:%M:%S').time()
                    print finalTime
                    #totalTime = totalTime + finalTime
                except:
                    pass

                toCheck =False
            counter += 1

print "total files: " + str(totalFiles)
#print "total time : " + str(totalTime)
