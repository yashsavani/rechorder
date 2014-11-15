#!/usr/bin/python

import util
import chordKMeans
import sys

# part 1

if len(sys.argv) == 1:
  midiFileName = 'default.mid'
else:
  midiFileName = sys.argv[1]

barLists = util.getNGramBarList(midiFileName)
for x in barLists:
  for y in x:
    print y.getKMeansFeatures()

#featureCentroids = chordKMeans.getFeatureCentroids(midiFileName)

# part 2... hopefully we'll get here


