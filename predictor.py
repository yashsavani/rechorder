#!/usr/bin/python

import util
import chordKMeans
import sys
import numpy as np

np.set_printoptions(formatter={'float': lambda x: '%.2f\t'%x})

# part 1

if len(sys.argv) == 1:
  midiFileName = 'default.mid'
else:
  midiFileName = sys.argv[1]

barLists = util.getNGramBarList(midiFileName)
for x in barLists:
  for y in x:
    print y.getKMeansFeatures()

featureCentroids = chordKMeans.getFeatureCentroids(midiFileName, 12)
print featureCentroids[0]
print featureCentroids[1]

# part 2... hopefully we'll get here


