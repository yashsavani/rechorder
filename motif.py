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

def generateAndWriteCentroids(midiFiles, numCentroids=kMeansDefault, beatsPerBar = beatsPerBarDefault):
  featureCentroids, centroidPoints = chordKMeans.getFeatureCentroids(midiFiles, numCentroids=numCentroids, beatsPerBar=beatsPerBar)
  filename = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(10)]) + '.mtf'
  print 'printing to', filename
  with open(filename, 'w') as f:
    for arr in featureCentroids:
      f.write(' '.join(map(str, arr.tolist())))
      f.write('\n')
  return filename

def readCentroids(filename):
  with open(filename, 'r') as f:
    mat = []
    for l in f:
      arr = []
      for x in l.split():
        arr.append(float(x))
      mat.append(arr)
    return np.matrix(mat)
  # catch exception?

