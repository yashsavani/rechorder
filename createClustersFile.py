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

beatsPerBarDefault = 8
kMeansDefault = 12

if len(sys.argv) == 1:
  midiFiles = ['default.mid']
else:
  midiFiles = sys.argv[1:]

fileName = motif.generateAndWriteCentroids(midiFiles, fileName = 'clusterCentroids.mtf', numCentroids = kMeansDefault, beatsPerBar = beatsPerBarDefault)
