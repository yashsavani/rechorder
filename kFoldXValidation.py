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
from makeTrainingSet import get_decision_function, generate_training_set
import visualizer

BEATS_PER_BAR = 1
PLOT_BEATS_PER_BAR = 1
N_PREVIOUS_BARS = 5


kMeansDefault = 12

#print centroids

def generateKFoldFiles():
  random.shuffle(midiFiles);
  run = len(midiFiles) // 10 # off by one? don't care atm
  for i in range(10):
    train = midiFiles[:i * run] + midiFiles[(i + 1) * run:]
    test = midiFiles[i * run : (i + 1) * run]
    yield (train, test)

def crossValidate():
  accuracy = []
  trainAccuracy = []
  for index, (trainMidiFiles, testMidiFiles) in enumerate(generateKFoldFiles()):
    centroidsFile = motif.generateAndWriteCentroids(midiFiles=trainMidiFiles, \
        numCentroids = kMeansDefault, beatsPerBar = BEATS_PER_BAR)
    centroids = motif.readCentroids(centroidsFile)
    
    # train svm on trainMidiFiles
    print "TRAINING... NUMBER", index
    xy_train = generate_training_set(n_previous_bars = N_PREVIOUS_BARS, k_means = kMeansDefault, beats_per_bar = BEATS_PER_BAR, midiFiles = trainMidiFiles, centroidVectors = centroids)
    decision_function = get_decision_function(xy_train, trainAccuracy)

    # test svm using testMidiFiles
    xy_test = generate_training_set(n_previous_bars = N_PREVIOUS_BARS, k_means = kMeansDefault, beats_per_bar = BEATS_PER_BAR, midiFiles = testMidiFiles, centroidVectors = centroids)
    
    '''NOTE: NOT EXACTLY 10 FOLD VALIDATION BECAUSE WE ARE ONLY USING THE FIRST SONG'''


    actual_y = xy_test[1]
    accuracy.append([])
    for approach in ["SVM", "Matching", "Repeat"]:
      predicted_y = []
      if approach == "SVM":
        predicted_y = decision_function(xy_test[0])
      elif approach == "Matching":
        truth = actual_y
        predictions = []
        for i, centroid in enumerate(truth):
          # to predict entry i, I'm only allowed to look at things i-1 or earlier.
          value = -1
          max_similar_sequence_length = 0
          for j in range(0, i-1):
            for k in range(j, -1, -1):
              if truth[k] != truth[i - 1 + k - j]:
                sequence_length = j - k
                if sequence_length > max_similar_sequence_length:
                  value = truth[j + 1]
                  max_similar_sequence_length = sequence_length
                break
          predictions.append(value)
        predicted_y = predictions

      

      else:
        predicted_y = [-1] + [i for i in actual_y[:-1]]

      n_correct = 0
      n_wrong = 0
      #print sum([a == b for a,b in zip(predicted_y, actual_y)])
      #print sum([a == b for a,b in zip(predicted_y, xy_test[1])])
      for prediction, actual in zip(predicted_y, actual_y):
        if prediction == actual:
          n_correct+=1
        else:
          n_wrong+=1

      predicted_y = [-1] * N_PREVIOUS_BARS + predicted_y
      actual_y = [0] * N_PREVIOUS_BARS + [i for i in actual_y]


      print '----------- Results of testing on hold-out set', index, 'with method', approach, '-----------'
      print 'n_correct :', n_correct
      print 'n_wrong   :', n_wrong
      print 'n_total   :', len(xy_test[0])
      print 'percent correct :', int((n_correct * 100 ) / len(xy_test[0])), '%'
      #visualizer.visualize(testMidiFiles[0], predicted_y, actual_y)
      accuracy[-1].append((n_correct * 100.0 ) / len(xy_test[0]))
  print "overall accuracy sequence:", accuracy
  print "trainAccuracy:", trainAccuracy
  print "A:", [sum(x) * 0.1 for x in zip(*accuracy)]
  print "B:", sum(trainAccuracy) * 0.1

if len(sys.argv) == 1:
  midiFiles = ['default.mid']
else:
  midiFiles = sys.argv[1:]
  crossValidate()
