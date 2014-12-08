#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import random

'''This file generates a training set to be used in our SVM,
 consisting of a list of previous-n -> current cluster pairings.

arguments: 
 - a sequence of songs
'''

n_previous_bars = 5
kMeans = 12
BEATS_PER_BAR = 1
PLOT_BEATS_PER_BAR = 1


if len(sys.argv) < 2:
  print "Please give me some MIDI files."
else:
  midiFiles = sys.argv[1:]
  centroidVectors, all_classifications = chordKMeans.getFeatureCentroids(midiFiles, numCentroids=kMeans, beatsPerBar=BEATS_PER_BAR)
  

  classification_sequences = []
  for midiFile in midiFiles:
    barLists = util.getNGramBarList(midiFile, n=BEATS_PER_BAR)
    bestBarList = barLists[0]

    this_sequence =[] # The sequence of cluster numbers for the current song
    for i, bar in enumerate(bestBarList):
      closestCentroid = chordKMeans.getClosestCentroidFromVector(centroidVectors, bar.getKMeansFeatures())
      this_sequence.append(closestCentroid)
    classification_sequences.append(this_sequence)

  output = []
  for sequence in classification_sequences:
    # want to cut up sequence into pieces of size n_previous_bars + 1
    for i in range(0, len(sequence) - n_previous_bars):
      history_numbers = sequence[i:i+n_previous_bars]
      current = sequence[i + n_previous_bars]
      history = []
      for j in range(n_previous_bars):
        history.extend([ int(history_numbers[j] == k) for k in range(kMeans) ])
      # history is just ones and zeros
      output.append([history, current])

  for history, current in output:
    print history, ":", current