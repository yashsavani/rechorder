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

BEATS_PER_BAR = 8
PLOT_BEATS_PER_BAR = 1

# begin visualization

if len(sys.argv) == 1:
  midiFiles = ['default.mid']
else:
  midiFiles = sys.argv[1:]

beatsPerBarDefault = 8
kMeansDefault = 12

#print centroids

def generateKFoldFiles():
  run = len(midiFiles) // 10 # off by one? don't care atm
  for i in range(10):
    train = midiFiles[:i * run] + midiFiles[(i + 1) * run:]
    test = midiFiles[i * run : (i + 1) * run]
    yield (train, test)

def getKFoldConfusionMatrices():
  for trainMidiFiles, testMidiFiles in generateKFoldFiles():
    centroidsFile = motif.generateAndWriteCentroids(midiFiles=trainMidiFiles, \
        numCentroids = kMeansDefault, beatsPerBar = beatsPerBarDefault)
    centroids = motif.readCentroids(centroidsFile)
    # train svm on trainMidiFiles

    # test svm using testMidiFiles


