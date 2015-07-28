#!/usr/bin/env python

import os
import glob
import sys
import json
import re
import numpy as np

INPUT_FOLDER = '/home/ubuntu/SETAnalysis/dataPool/'
INT_PARAM = 'CHANGE_VALUE'
WIN_SIZE = 25

def warning(objs):
    sys.stderr.write("WARNING: " + objs + "\n")

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime, reverse=True))
    
def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    # get subfolders
    if len(sys.argv) != 3:
        warning("Parameter stock name and win size are required!")
        exit()

    subFolders = sorted_ls(INPUT_FOLDER)
    keyWord = sys.argv[1].upper()
    print(keyWord),
    
    WIN_SIZE = int(sys.argv[2])
    
    totalList = []
    reliability = 0
    
    # Loop to read throught every object
    for intCounter in range(0, len(subFolders), WIN_SIZE):
        # Loop to get the interseting parameter in a certain window size
        valueList = []
        for eachDay in range(WIN_SIZE):
            # Check to make sure that reading data is in range 
            if intCounter + eachDay < len(subFolders):
                # Create a target file name
                targetFile = glob.glob(INPUT_FOLDER + subFolders[intCounter + eachDay] + '/stock_data/*' + keyWord + '.json')
               	
                # Check that object is exist!
                if len(targetFile) > 1 or len(targetFile) == 0:
                    warning("Object of " + keyWord + " not found on " + subFolders[intCounter + eachDay])
                    reliability += 1
                    continue
     

                payload = [line.rstrip('\n') for line in open(targetFile[0])]
                stockObject = json.loads(payload[0])

                # Check for object again                
                if stockObject['SYMBOL'] == keyWord:
                    # Read object
                    # print(str(stockObject) + "\n")
                    if isFloat(stockObject[INT_PARAM]) == False:
                        warning("Number of object " + subFolders[intCounter + eachDay] + " is not a number (" + stockObject[INT_PARAM] + ")")
                        valueList.append(0.0)
                        continue
                        
                    valueList.append(float(stockObject[INT_PARAM]))
                else:
                    warning("Object name and content mismated!")
                    print("\tError\tMiss\tMatch")
                    exit(-1)
        
        # Calculate region
        # print(valueList)
        totalList.append(np.mean(valueList))
    
    # Processing
    _max = np.max(totalList)
    _min = np.min(totalList)
    _diffR = _max - _min

    for i in range(len(totalList)):
        totalList[i] *= float(float(i) / float(len(totalList))) * 0.6
        # print("fr: " + str(float(float(i) / float(len(totalList))) * 0.6)),
    
    # Final Score
    if len(totalList) > 0:
        print("\t{:.5f}".format(np.mean(totalList))),
    else:
        print("\tNoResult"),
    totalF = len(subFolders)

    print("\t" + str(totalF - reliability) + "/" + str(totalF) + "\t" + str(float(totalF - reliability) / float(totalF) * 100)),
    '''
    for i in range(len(totalList)):
        print("\t{:.5f}".format(totalList[i])),
    '''
    print("")
