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
from operator import itemgetter

'''This file generates a training set to be used in our SVM,
 consisting of a list of previous-n -> current cluster pairings.

arguments: 
 - a sequence of songs
'''

N_PREVIOUS_BARS = 5
kMeans = 7
BEATS_PER_BAR = 4


def generate_training_set(n_previous_bars, k_means, beats_per_bar, midiFiles, centroidVectors):
  #centroidVectors, all_classifications = chordKMeans.getFeatureCentroids(midiFiles, numCentroids=kMeans, beatsPerBar=BEATS_PER_BAR)
  #centroidVectors = motif.readCentroids(cluster_centroids_file)

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

def argmax(l):
  index, value = max(enumerate(l), key = itemgetter(1))
  return index

def get_decision_function(xy, accuracy = None):

  lin_clf = svm.LinearSVC()
  lin_clf.fit(xy[0], xy[1])
  def decision(featureTable):
    return [argmax(confidence) for confidence in lin_clf.decision_function(featureTable)]

  predicted_y = decision(xy[0])
  n_correct = 0
  n_wrong = 0

  #print predicted_y
  #print xy[1]
  for prediction, actual in zip(predicted_y, xy[1]):
      if prediction == actual:
        n_correct+=1
      else:
        n_wrong+=1

  print '****-----------Results of testing on training set-----------'
  print 'n_correct :', n_correct
  print 'n_wrong   :', n_wrong
  print 'n_total   :', len(xy[0])
  print "accuracy: ", float(n_correct) / (n_correct + n_wrong)
  if accuracy != None:
    accuracy.append(float(n_correct) / (n_correct + n_wrong))

  return decision

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Please give me some MIDI files."
  else:
    midiFiles = sys.argv[1:]
    centroidVectors, all_classifications = chordKMeans.getFeatureCentroids(midiFiles, numCentroids=kMeans, beatsPerBar=BEATS_PER_BAR)
    xy = generate_training_set(N_PREVIOUS_BARS, kMeans, BEATS_PER_BAR, midiFiles, centroidVectors)
    decision_function = get_decision_function(xy)

    predicted_y = decision_function(xy[0])
    n_correct = 0
    n_wrong = 0

    #print predicted_y
    #print xy[1]
    for prediction, actual in zip(predicted_y, xy[1]):
        if prediction == actual:
          n_correct+=1
        else:
          n_wrong+=1

    print '****-----------Results of testing on training set-----------'
    print 'n_correct :', n_correct
    print 'n_wrong   :', n_wrong
    print 'n_total   :', len(xy[0])
    print "accuracy: ", float(n_correct) / (n_correct + n_wrong)

