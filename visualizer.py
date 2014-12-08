#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import random

BEATS_PER_BAR = 1
PLOT_BEATS_PER_BAR = 1

def plotRectangle(plot, top, left, right, height, opt='', alpha=1):
  x = np.array([left, left, right, right])
  y = np.array([float(top)] * 4)
  y[0] -= height
  y[3] -= height
  plot.fill(x, y, opt, alpha=alpha)

def plotPianoKeys(plot, centroids, row, totalRows):
  n = len(centroids)
  plt.axis([0, 1, 0, 1])
  x = np.linspace(0, 1)
  top = (row + 1.) / totalRows
  height = 1. / totalRows - 0.01

  # normalize the keys
  norm = np.linalg.norm(centroids[row])
  if norm != 0:
    normalizeKeys = np.array([c / float(norm) for c in centroids[row]])
  else:
    normalizeKeys = np.array(centroids[row])

  # white keys
  whiteKeyPos = [0, 2, 4, 5, 7, 9, 11]
  for i in range(7):
    color = 'w' if centroids[row][whiteKeyPos[i]] == 0 else 'r'
    plotRectangle(plot, top, i / 7., (i + 1) / 7., height, 'w')
    plotRectangle(plot, top, i / 7., (i + 1) / 7., height, color, alpha=normalizeKeys[i])

  # black keys
  blackKeyPos = [1, 3, 6, 8, 10]
  left = [x + 2. / 3 for x in [0, 1, 3, 4, 5]]
  for i in range(len(left)):
    l = left[i]
    p = int(round(normalizeKeys[blackKeyPos[i]] * 255.))
    color = '#%0.2x0000' % p
    plotRectangle(plot, top, l / 7., (l + 0.666) / 7, height * 0.6, color)

def visualize(midiFile, predictedClusters, truth):

  other_colors = []
  for x in range(100):
    c = "#"
    for _ in range(6):
      c += random.choice('1234567890ABCDEF')
    other_colors.append(c);
  

  totalBars = len(truth)
  for i, closestCentroid in enumerate(truth):
    #x = np.linspace(0 - (i - 0.5) / float(totalBars), (i + 0.5) / float(totalBars) + 100, 2)
    x = np.array([i / float(totalBars), i / float(totalBars), (i + 1) / float(totalBars), (i + 1) / float(totalBars)])
    y = np.array([200] * 4)
    y[0] = 0
    y[3] = 0
    #closestCentroid = centroidPoints[i]
    #print len(other_colors), centroidPoints[i], "::", other_colors[closestCentroid % len(other_colors)]
    p = plt.fill(x, y, other_colors[closestCentroid % len(other_colors)], alpha=0.2)
    #plt.grid(True)

  # plot each beat individually
  barLists = util.getNGramBarList(midiFile, n=PLOT_BEATS_PER_BAR)
  bestBarList = barLists[0]
  #totalBars = len(bestBarList)
  for i, bar in enumerate(bestBarList):
    for beat in bar.beats:
      for note, duration in beat:
        x = np.array([i / float(totalBars), i / float(totalBars), (i + 1) / float(totalBars), (i + 1) / float(totalBars)])
        #x = np.linspace(i / float(totalBars), (i + 1) / float(totalBars), 4)
        y = np.array([float(note)] * 4)
        y[0] = y[0] - 1
        y[3] = y[3] - 1
        #y[0] = y[0] - duration
        #y[3] = y[3] - duration
        p = plt.fill(x, y, 'r', alpha = duration ** 2)
        #print duration

  plt.axis([0, 1, 0, util.NUM_NOTES])
  plt.xlabel('time')
  plt.ylabel('note')
  plt.title('Clustering of musical bars vs time')
  
  totalBars = len(predictedClusters)
  for i, centroid in enumerate(predictedClusters):
    if centroid == -1:
      continue
    #x = np.linspace(0 - (i - 0.5) / float(totalBars), (i + 0.5) / float(totalBars) + 100, 2)
    x = np.array([i, i, (i + 1), (i + 1)])
    x = x / float(totalBars)
    y = np.array([10] * 4)
    y[0] = 0
    y[3] = 0
    if centroid == truth[i]:
      y[1] = 15
      y[2] = 15
    #closestCentroid = truth[i]
    #print len(other_colors), truth[i], "::", other_colors[closestCentroid % len(other_colors)]
    p = plt.fill(x, y, other_colors[centroid % len(other_colors)])


  plt.show()


# begin visualization


if __name__ == "__main__":
  if len(sys.argv) == 1:
    midiFiles = ['default.mid']
  else:
    midiFiles = sys.argv[1:]

  kMeans = 7



  for midiFile in midiFiles:
    barLists = util.getNGramBarList(midiFile, n=BEATS_PER_BAR)
    '''
    for x in barLists:
      for y in x:
        print y
    '''

    featureCentroids, centroidPoints = chordKMeans.getFeatureCentroids(midiFiles, numCentroids=kMeans, beatsPerBar=BEATS_PER_BAR)

    #fig = plt.figure(figsize=(7, 2 * kMeans))
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect(3.5 / 8. * kMeans)

    for i in range(len(featureCentroids)):
      plotPianoKeys(ax, featureCentroids, i, kMeans)
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.show()

    plt.matshow(featureCentroids)
    plt.show()

    bestBarList = barLists[0]
    totalBars = len(bestBarList)

    #print featureCentroids
    #print centroidPoints
    print "cluster sizes:"
    counts = []
    for k in range(kMeans):
      count = 0
      for x in centroidPoints:
        if k==x:
          count += 1
      counts.append(count)
    m = max(counts)
    for i, x in enumerate(counts):
      print "%2d:" %(i),
      print "-" * ((x * 40) / m) 

    
    colors = list('bgrcmyk')
    #other_colors = list('bgrcmyk')
    other_colors = []
    for x in range(100):
      c = "#"
      for _ in range(6):
        c += random.choice('1234567890ABCDEF')
      other_colors.append(c);

    # create a palette.
    color = {}
    for i, bar in enumerate(bestBarList):
      closestCentroid = chordKMeans.getClosestCentroidFromVector(featureCentroids, bar.getKMeansFeatures())
      if len(colors) > 0:
        if closestCentroid not in color:
          color[closestCentroid] = colors.pop(0) + ""
      else:
        color[closestCentroid] = 'w'

    # This is where we draw the large vertical bars.

    truth = []
    predictedClusters = []
    for i, bar in enumerate(bestBarList):
      closestCentroid = chordKMeans.getClosestCentroidFromVector(featureCentroids, bar.getKMeansFeatures())
      truth.append(closestCentroid)

    '''
    print "length of background bars:", len(bestBarList)
    for i, bar in enumerate(bestBarList):
      closestCentroid = chordKMeans.getClosestCentroidFromVector(featureCentroids, bar.getKMeansFeatures())
      #x = np.linspace(0 - (i - 0.5) / float(totalBars), (i + 0.5) / float(totalBars) + 100, 2)
      x = np.array([i / float(totalBars), i / float(totalBars), (i + 1) / float(totalBars), (i + 1) / float(totalBars)])
      y = np.array([200] * 4)
      y[0] = 0
      y[3] = 0
      #closestCentroid = centroidPoints[i]
      #print len(other_colors), centroidPoints[i], "::", other_colors[closestCentroid % len(other_colors)]
      p = plt.fill(x, y, other_colors[closestCentroid % len(other_colors)], alpha=0.2)
      #plt.grid(True)


    # plot each beat individually
    barLists = util.getNGramBarList(midiFile, n=PLOT_BEATS_PER_BAR)
    bestBarList = barLists[0]
    totalBars = len(bestBarList)
    for i, bar in enumerate(bestBarList):
      for beat in bar.beats:
        for note, duration in beat:
          x = np.array([i / float(totalBars), i / float(totalBars), (i + 1) / float(totalBars), (i + 1) / float(totalBars)])
          #x = np.linspace(i / float(totalBars), (i + 1) / float(totalBars), 4)
          y = np.array([float(note)] * 4)
          y[0] = y[0] - 1
          y[3] = y[3] - 1
          #y[0] = y[0] - duration
          #y[3] = y[3] - duration
          p = plt.fill(x, y, 'r', alpha = duration ** 2)
          #print duration

    plt.axis([0, 1, 0, util.NUM_NOTES])
    plt.xlabel('time')
    plt.ylabel('note')
    plt.title('Clustering of musical bars vs time')
    #plt.show() # moved this to later


    # part 2... hopefully we'll get here
    # idea right now is to purely examine the sequence of clusters 
    # and search for the longest consecutive string of clusters that match the currently most recent string of clusters.
    

    barLists = util.getNGramBarList(midiFile, n=BEATS_PER_BAR)
    bestBarList = barLists[0]
    totalBars = len(bestBarList)
    truth = []
    for i, bar in enumerate(bestBarList):
      closestCentroid = chordKMeans.getClosestCentroidFromVector(featureCentroids, bar.getKMeansFeatures())
      truth.append(closestCentroid)

'''
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

    visualize(midiFile, predictions, truth)
'''
    print truth
    print predictions
    n_correct = 0
    n_wrong = 0
    n_unknown = 0
    for a,b in zip(truth, predictions):
      if b == -1:
        n_unknown +=1
        print "?",
      elif a == b:
        n_correct +=1
        print "Y",
      else:
        n_wrong += 1
        print "N",
    print ""
    print "correct:", n_correct
    print "wrong:", n_wrong
    print "no guess", n_unknown

    totalBars = len(predictions)

    for i, centroid in enumerate(predictions):
      if centroid == -1:
        continue
      #x = np.linspace(0 - (i - 0.5) / float(totalBars), (i + 0.5) / float(totalBars) + 100, 2)
      x = np.array([i, i, (i + 1), (i + 1)])
      x = x / float(totalBars)
      y = np.array([10] * 4)
      y[0] = 0
      y[3] = 0
      if centroid == truth[i]:
        y[1] = 15
        y[2] = 15
      #closestCentroid = truth[i]
      #print len(other_colors), truth[i], "::", other_colors[closestCentroid % len(other_colors)]
      p = plt.fill(x, y, other_colors[centroid % len(other_colors)])


    plt.show()
    print "length of predictions:", len(predictions)
    '''




