#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab
import random

# part 1

if len(sys.argv) == 1:
  midiFiles = ['default.mid']
else:
  midiFiles = sys.argv[1:]

for midiFile in midiFiles:
  barLists = util.getNGramBarList(midiFile, n=4)
  '''
  for x in barLists:
    for y in x:
      print y
  '''

  featureCentroids, centroidPoints = chordKMeans.getFeatureCentroids(midiFiles)

  bestBarList = barLists[0]
  totalBars = len(bestBarList)

  #print featureCentroids
  #print centroidPoints
  print "cluster sizes:"
  counts = []
  for k in range(12):
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
  other_colors = list('bgrcmyk')
  for x in range(100):
    c = "#"
    for _ in range(6):
      c += random.choice('1234567890ABCDEF')
    other_colors.append(c);

  color = {}
  for i, bar in enumerate(bestBarList):
    closestCentroid = chordKMeans.getClosestCentroid(featureCentroids, bar.getKMeansFeatures(), 0)
    if len(colors) > 0:
      if closestCentroid not in color:
        color[closestCentroid] = colors.pop(0) + ""
    else:
      color[closestCentroid] = 'w'


  for i, bar in enumerate(bestBarList):
    closestCentroid = chordKMeans.getClosestCentroid(featureCentroids, bar.getKMeansFeatures(), 0)
    #x = np.linspace(0 - (i - 0.5) / float(totalBars), (i + 0.5) / float(totalBars) + 100, 2)
    x = np.array([i / float(totalBars), i / float(totalBars), (i + 1) / float(totalBars), (i + 1) / float(totalBars)])
    y = np.array([200] * 4)
    y[0] = 0
    y[3] = 0
    closestCentroid = centroidPoints[i]
    #print len(other_colors), centroidPoints[i], "::", other_colors[closestCentroid % len(other_colors)]
    p = plt.fill(x, y, other_colors[closestCentroid % len(other_colors)], alpha=0.2)
    #plt.grid(True)


  # plot each beat individually
  for i, bar in enumerate(bestBarList):
    for beat in bar.beats:
      for note, duration in beat:
        x = np.linspace(i / float(totalBars), (i + 1) / float(totalBars), 2)
        y = np.zeros(2)
        y[0] = note
        y[1] = note
        p = plt.plot(x, y, 'r')
        #print duration
        pylab.setp(p, linewidth = duration * 5)

  plt.axis([0, 1, 0, util.NUM_NOTES])
  plt.xlabel('time')
  plt.ylabel('note')
  plt.title('Clustering of musical bars vs time')
  plt.show()

  # part 2... hopefully we'll get here


