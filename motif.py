#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import random

beatsPerBarDefault = 8
kMeansDefault = 12

def generateAndWriteCentroids(midiFiles, numCentroids=kMeansDefault, beatsPerBar = beatsPerBarDefault, fileName = None):
  featureCentroids, centroidPoints = chordKMeans.getFeatureCentroids(midiFiles, numCentroids=numCentroids, beatsPerBar=beatsPerBar)
  if not fileName:
    # make a random name
    fileName = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)]) + '.mtf'
  print 'printing to', fileName
  with open(fileName, 'w') as f:
    for arr in featureCentroids:
      f.write(' '.join(map(str, arr.tolist())))
      f.write('\n')
  return fileName

def readCentroids(fileName):
  with open(fileName, 'r') as f:
    mat = []
    for l in f:
      arr = []
      for x in l.split():
        arr.append(float(x))
      mat.append(arr)
    return np.matrix(mat)
  # catch exception?

