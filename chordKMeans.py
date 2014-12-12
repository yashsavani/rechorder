#!/usr/bin/python
import util
import numpy as np
import random
import sys

#np.set_printoptions(formatter={'float': lambda x: '%.2f\t'%round(x,2)})

def getBestBarList(midiFileName, beatsPerBar=4):
    barLists = util.getNGramBarList(midiFileName, n=beatsPerBar)
    return barLists[0]
    #return best bar list in barLists

# gets a list of euclidean distances between the rows of mat_a and index_mat[index]
def euclideanDistance(mat_a, index_mat, index) :
    diff_mat = np.subtract(mat_a, np.tile(index_mat[index], (mat_a.shape[0], 1)))
    dists = [np.linalg.norm(vec) for vec in diff_mat]
    return dists

# gets a list of cosine distances between the rows of mat_a and index_mat[index]
def cosineDistance(mat_a, index_mat, index) :
    dot_mat = np.dot(mat_a, index_mat[index].reshape(-1,1)).transpose()
    dists = [dot_mat[0,i] / (np.linalg.norm(mat_a[i]) * np.linalg.norm(index_mat[index])) for i in range(dot_mat.shape[1])]
    return dists

# gets the closest centroid to the vector in the data_mat
def getClosestCentroid(centroids_mat, data_mat, index) :
    dists = euclideanDistance(centroids_mat, data_mat, index)
    return np.argmin(dists)

def getClosestCentroidFromVector(centroids_mat, vector):
    return getClosestCentroid(centroids_mat, [vector], 0)

def getFeatureCentroids(midiFiles, beatsPerBar=4, numCentroids=12, maxIterations=100): # basically k-means
    bestBarList = []
    for midiFileName in midiFiles :
        bestBarList += getBestBarList(midiFileName, beatsPerBar=beatsPerBar)
    numExamples = len(bestBarList)

    # parse bars into a data matrix
    data_mat = np.array([bar.getKMeansFeatures() for bar in bestBarList])

    # list of 12-vectors
    print 'Running k-Means.'
    # initialize the k clusters from k randomly chosen points in the data
    indices = range(numExamples)
    random.shuffle(indices)
    centroids_mat = data_mat[indices[:numCentroids]]

    iterations = 0
    corr_centers = [-1]*numExamples
    n_dashes = 0
    print "progress:",
    for _ in range(maxIterations) :
        if _ * 40 / maxIterations > n_dashes:
            for i in range(((_ * 40) / maxIterations) - n_dashes):
                sys.stdout.write('-')
                sys.stdout.flush()
                n_dashes += 1
        iterations += 1
        corr_points = [[] for placeholder in range(numCentroids)]
        new_corr_centers = []
        # Find closest cluster centers for each point
        for index in range(numExamples) :
            center = getClosestCentroid(centroids_mat, data_mat, index)
            new_corr_centers.append(center)
            corr_points[center].append(index)

        # Move cluster center to center of corresponding points
        for index in range(numCentroids) :
            rel_points = data_mat[corr_points[index]].transpose()
            centroids_mat[index] = np.array([np.mean(pt_points) if pt_points.any() else 0 for pt_points in rel_points])

        if new_corr_centers == corr_centers :
            break

        corr_centers = list(new_corr_centers)
    print ""
    return (centroids_mat, corr_centers)

def evaluateKmeansClusters(midiFiles, centroids, corr_centers) :
    bestBarList = []
    for midiFileName in midiFiles :
        bestBarList += getBestBarList(midiFileName)
    numExamples = len(bestBarList)
    numCentroids = centroids.shape[0]

    # parse bars into a data matrix
    data_mat = np.array([bar.getKMeansFeatures() for bar in bestBarList])

    def silhouette(index) :
        same_cntr_pts = data_mat[[i for i, x in enumerate(corr_centers) if x == corr_centers[index]]]
        a_i = np.mean(euclideanDistance(same_cntr_pts, data_mat, index))

        diff_centroids = centroids[[i for i in range(numCentroids) if i != corr_centers[index]]]
        b_i = np.min(euclideanDistance(diff_centroids, data_mat, index))

        return (b_i - a_i) / max(a_i, b_i)

    return np.mean([silhouette(i) for i in range(numExamples)])

