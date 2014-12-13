#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import random

beatsPerBarDefault = 4
kMeansDefault = 7


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

if __name__ == "__main__":
  if len(sys.argv) <= 2:
    print "Please give filename and the midi files."
    sys.exit(1)
  else:
    filename = sys.argv[1]+".mtf"
    midiFiles = sys.argv[2:]
  num_reps = 5
  centers = [chordKMeans.getFeatureCentroids(midiFiles, numCentroids=kMeansDefault, beatsPerBar=beatsPerBarDefault) for _ in range(num_reps)]
  results = [chordKMeans.evaluateKmeansClusters(midiFiles, centroids, corr_centers) \
        for (centroids, corr_centers) in centers]
  enum = [(e,z) for e,z in enumerate(results)]

  featureCentroids = centers[max(enum, key=lambda x: x[1])[0]][0]

  print 'writing to', filename
  with open(filename, 'w') as f:
    for arr in featureCentroids:
      f.write(' '.join(map(str, arr.tolist())))
      f.write('\n')



