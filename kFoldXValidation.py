#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import random
import motif

BEATS_PER_BAR = 4
PLOT_BEATS_PER_BAR = 1

if len(sys.argv) <= 2:
  print "Please give motif file and the midi files."
  sys.exit(1)
else:
  mtffile = sys.argv[1]
  midiFiles = sys.argv[2:]

beatsPerBarDefault = 4
kMeansDefault = 12

def generateKFoldFiles():
  run = len(midiFiles) // 10 # off by one? don't care atm
  for i in range(10):
    train = midiFiles[:i * run] + midiFiles[(i + 1) * run:]
    test = midiFiles[i * run : (i + 1) * run]
    yield (train, test)

def getKFoldConfusionMatrices(mtffile):
  for trainMidiFiles, testMidiFiles in generateKFoldFiles():
    # centroidsFile = motif.generateAndWriteCentroids(midiFiles=trainMidiFiles, \
    #     numCentroids = kMeansDefault, beatsPerBar = beatsPerBarDefault)
    centroids = motif.readCentroids(mtffile)

    # train supervised learning algorithm on trainMidiFiles

    # test supervised learning algorithm using testMidiFiles

print getKFoldConfusionMatrices(mtffile)
