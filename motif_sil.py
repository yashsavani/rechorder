#!/usr/bin/python
import util
import chordKMeans
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(formatter={'float': lambda x: '%.2f\t'%x})

# part 1

if len(sys.argv) == 1:
    midiFiles = ['default.mid']
else:
    midiFiles = sys.argv[1:]


for i in range(4,20) :
    print "for k = %s"%i
    num_reps = 5
    centers = [chordKMeans.getFeatureCentroids(midiFiles, numCentroids=i) for _ in range(num_reps)]
    results = [chordKMeans.evaluateKmeansClusters(midiFiles, centroids, corr_centers) \
            for (centroids, corr_centers) in centers]

    plt.plot(i, np.mean(results), marker='o', color='b')
    plt.errorbar(i, np.mean(results), yerr=np.std(results), fmt="-", color='b')

plt.axis([0,11,0,1])
plt.xlabel("k")
plt.ylabel("average silhouette value")
plt.title("Best k for kmeans on music analysis")
plt.show()

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


# Running Markov model for now
print "testing out Markov model."
k = 12
labelSeries = featureCentroids[1]
model = buildMarkovModel(labelSeries, k)
print "----labelSeries----"
print labelSeries
print "------model:-------"
for prior, distribution in enumerate(model):
    print "given", prior, "distribution is", map(prettyfloat, distribution)


IS_REPEAT = 0
NOT_REPEAT = 1
CORRECT = 1
WRONG = 0

stats = [[0,0],[0,0]]

for before, after in zip(labelSeries[:-1], labelSeries[1:]):
    prediction = makeRandomPrediction(model, before)
    print "before:", before, "     prediction:", prediction, "   actual:", after,
    if prediction == after:
        print "win!"
    else:
        print ""

    repeat = NOT_REPEAT
    if before == after:
        repeat = IS_REPEAT

    correct = WRONG
    if makeRandomPrediction(model, before) == after:
        correct = CORRECT

    stats[correct][repeat]+=1
print "for repeats:", stats[CORRECT][IS_REPEAT], "correct,", stats[WRONG][IS_REPEAT], "wrong.", stats[CORRECT][IS_REPEAT] * 1.0 / (stats[CORRECT][IS_REPEAT]+stats[WRONG][IS_REPEAT]),"%"
print "for non-repeats:", stats[CORRECT][NOT_REPEAT], "correct,", stats[WRONG][NOT_REPEAT], "wrong.", stats[CORRECT][NOT_REPEAT] * 1.0 / (stats[WRONG][NOT_REPEAT]+stats[CORRECT][NOT_REPEAT]), "%" 

# part 2... hopefully we'll get here


