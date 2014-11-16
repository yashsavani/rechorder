#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

# part 1

if len(sys.argv) == 1:
  midiFileName = 'default.mid'
else:
  midiFileName = sys.argv[1]

barLists = util.getNGramBarList(midiFileName, n=4)
'''
for x in barLists:
  for y in x:
    print y
'''


#featureCentroids = chordKMeans.getFeatureCentroids(midiFileName)

bestBarList = barLists[0]

totalBars = len(bestBarList)
print totalBars

for bar in bestBarList:
  print bar

# plot each beat individually
for i, bar in enumerate(bestBarList):
  for beat in bar.beats:
    for note, duration in beat:
      x = np.linspace(i / float(totalBars), (i + 1) / float(totalBars), 2)
      y = np.zeros(2)
      y[0] = note
      y[1] = note
      p = plt.plot(x, y, 'r')
      pylab.setp(p, linewidth = duration * 5)

plt.axis([0, 1, 0, util.NUM_NOTES])
plt.show()

# part 2... hopefully we'll get here


