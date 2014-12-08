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
  for index, (trainMidiFiles, testMidiFiles) in enumerate(generateKFoldFiles()):
    centroidsFile = motif.generateAndWriteCentroids(midiFiles=trainMidiFiles, \
        numCentroids = kMeansDefault, beatsPerBar = BEATS_PER_BAR)
    centroids = motif.readCentroids(centroidsFile)
    
    # train svm on trainMidiFiles
    xy_train = generate_training_set(n_previous_bars = N_PREVIOUS_BARS, k_means = kMeansDefault, beats_per_bar = BEATS_PER_BAR, midiFiles = trainMidiFiles, centroidVectors = centroids)
    decision_function = get_decision_function(xy_train)

    # test svm using testMidiFiles
    xy_test = generate_training_set(n_previous_bars = N_PREVIOUS_BARS, k_means = kMeansDefault, beats_per_bar = BEATS_PER_BAR, midiFiles = testMidiFiles[0:1], centroidVectors = centroids)
    
    '''NOTE: NOT EXACTLY 10 FOLD VALIDATION BECAUSE WE ARE ONLY USING THE FIRST SONG'''


    predicted_y = decision_function(xy_test[0])
    actual_y = xy_test[1]

    n_correct = 0
    n_wrong = 0
    for prediction, actual in zip(predicted_y, xy_test[1]):
      if prediction == actual:
        n_correct+=1
      else:
        n_wrong+=1
    print '----------- Results of testing on hold-out set', index, '-----------'
    print 'n_correct :', n_correct
    print 'n_wrong   :', n_wrong
    print 'n_total   :', len(xy_test[0])
    print 'percent correct :', int((n_correct * 100 ) / len(xy_test[0])), '%'
    visualizer.visualize(testMidiFiles[0], predicted_y, actual_y)
    accuracy.append((n_correct * 100.0 ) / len(xy_test[0]))
  print "overall accuracy sequence:", accuracy

if len(sys.argv) == 1:
  midiFiles = ['default.mid']
else:
  midiFiles = sys.argv[1:]
  crossValidate()
