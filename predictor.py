#!/usr/bin/python

import util
import chordKMeans
import sys
import random
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

for i in range(20) :
	featureCentroids = chordKMeans.getFeatureCentroids(midiFileName, 12)
	print "for k = %s"%i
	print chordKMeans.evaluateKmeansClusters(midiFileName, featureCentroids[0], featureCentroids[1])


# want to, given new Midi
def buildMarkovModel(labelSeries, k):
	'''
	Assumes that label series is a sequence of integers in 0, ..., k-1.
	also assumes that labelSeries is nonempty
	'''
	model = [[1 for i in range(k)] for j in range(k)]
	for i in range(len(labelSeries) - 1):
		before = labelSeries[i]
		after  = labelSeries[i+1]
		model[before][after] += 1

	for i in range(k):
		n = sum(model[i])
		for j in range(k):
			model[i][j] *= 1.0 / n

	return model

def makeRandomPrediction(model, before):
	'''
	model: a k by k list of lists of floats.
	model[i] should sum up to 1 for all i.

	before: an integer between 0 and k-1 inclusive.

	There are ways to make this happen in log(k) rather than k time but we won't do this now.
	'''
	probability_distribution = model[before]
	# this should sum up to 1 and be nonnegative.

	continuous_choice = random.random()
	for i, probability in enumerate(probability_distribution):
		if probability >= continuous_choice:
			return i
		else:
			continuous_choice -= probability
	#If you're here there's a problem
	return "There's an error in prediction"

class prettyfloat(float):
    def __repr__(self):
        return "%0.2f" % self

# testing out Markov model
print "testing out Markov model."
k = 5
labelSeries = [0,1,2,3,4] * 10 + [0, 1, 2] * 10
model = buildMarkovModel(labelSeries, k)
print "----labelSeries----"
print labelSeries
print "------model:-------"
for prior, distribution in enumerate(model):
	print "given", prior, "distribution is", map(prettyfloat, distribution)

print "----predictions----"
for prior in range(k):
	print "given prior", prior, "model randomly predicts", makeRandomPrediction(model, prior)


# part 2... hopefully we'll get here


