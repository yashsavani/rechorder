#!/usr/bin/python
import util
import numpy as np

def getBestBarList(midiFileName):
  barLists = util.getNGramBarList(midiFileName)
  #return best bar list in barLists

def getFeatureCentroids(midiFileName, numCentroids=12): # basically k-means
  bestBarList = getBestBarList(midiFileName)

