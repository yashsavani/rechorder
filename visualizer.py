#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

# part 1

if len(sys.argv) == 1:
  midiFiles = ['default.mid']
else:
  midiFiles = sys.argv[1:]

barLists = util.getNGramBarList(midiFiles, n=4)
'''
for x in barLists:
  for y in x:
    print y
'''

featureCentroids, centroidAssignments = chordKMeans.getFeatureCentroids(midiFiles)

bestBarList = barLists[0]
print len(bestBarList), bestBarList
totalBars = len(bestBarList)

print featureCentroids[0]

colors = list('bgrcmyk')
color = {}
print totalBars
print centroidAssignments
for i, bar in enumerate(bestBarList):
  closestCentroid = chordKMeans.getClosestCentroid(featureCentroids, bar.getKMeansFeatures(), 0)
  closestCentroid = centroidAssignments[i]
  if len(colors) > 0:
    if closestCentroid not in color:
      color[closestCentroid] = colors.pop(0)
  else:
    color[closestCentroid] = 'r'

print color

for i, bar in enumerate(bestBarList):
  closestCentroid = chordKMeans.getClosestCentroid(featureCentroids, bar.getKMeansFeatures(), 0)

  #closestCentroid2 is supposed to equal closestCentroid, but it doesn't
  closestCentroid = centroidAssignments[i]
  
  #x = np.linspace(0 - (i - 0.5) / float(totalBars), (i + 0.5) / float(totalBars) + 100, 2)
  x = np.array([i / float(totalBars), i / float(totalBars), (i + 1) / float(totalBars), (i + 1) / float(totalBars)])
  y = np.array([200] * 4)
  y[0] = 0
  y[3] = 0
  p = plt.fill(x, y, color[closestCentroid], alpha=0.2)
  #plt.grid(True)



for bar in bestBarList:
  pass #print bar

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
plt.show()

# part 2... hopefully we'll get here


