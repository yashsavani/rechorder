#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import random
from sklearn import svm

'''This file generates a training set to be used in our SVM,
 consisting of a list of previous-n -> current cluster pairings.

arguments: 
 - a sequence of songs
'''

N_PREVIOUS_BARS = 5
kMeans = 12
BEATS_PER_BAR = 1


def generate_training_set(n_previous_bars, k_means, beats_per_bar, midiFiles):
  centroidVectors, all_classifications = chordKMeans.getFeatureCentroids(midiFiles, numCentroids=kMeans, beatsPerBar=BEATS_PER_BAR)
  

  classification_sequences = []
  for midiFile in midiFiles:
    barLists = util.getNGramBarList(midiFile, n=beats_per_bar)
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
        history.extend([ int(history_numbers[j] == k) for k in range(k_means) ])
      # history is just ones and zeros
      output.append([history, current])

  '''for history, current in output:
    print history, ":", current'''

  lin_clf = svm.LinearSVC()
  xy = zip(*output)
  return xy

def get_decision_function(xy):

  lin_clf = svm.LinearSVC()
  lin_clf.fit(xy[0], xy[1])
  return lin_clf.decision_function

if len(sys.argv) < 2:
  print "Please give me some MIDI files."
else:
  midiFiles = sys.argv[1:]
  xy = generate_training_set(N_PREVIOUS_BARS, kMeans, BEATS_PER_BAR, midiFiles)
  decision_function = get_decision_function(xy)

  predicted_y = decision_function(xy[0])
  n_correct = 0
  n_wrong = 0

  #print predicted_y
  #print xy[1]
  for probabilities, i in zip(predicted_y, xy[1]):
    if probabilities[i] == max(probabilities):
      n_correct+=1
    else:
      n_wrong+=1
  print 'n correct:', n_correct, 'n_wrong:', n_wrong


  print decision_function(xy[0][0:1]), 'length:', len(xy[0])

