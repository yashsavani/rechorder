#!/usr/bin/python
import util
import numpy as np
import random

np.set_printoptions(formatter={'float': lambda x: '%.2f\t'%round(x,2)})

def getBestBarList(midiFileName):
	barLists = util.getNGramBarList(midiFileName)
	return barLists[0]
	#return best bar list in barLists

def getFeatureCentroids(midiFileName, numCentroids=12, maxIterations=100): # basically k-means
	bestBarList = getBestBarList(midiFileName)
	numExamples = len(bestBarList)

	# parse bars into a data matrix
	data_mat = np.array([bar.getKMeansFeatures() for bar in bestBarList])

	# initialize the k clusters from k randomly chosen points in the data
	indices = range(numExamples)
	random.shuffle(indices)
	centroids_mat = data_mat[indices[:numCentroids]]

	iterations = 0
	corr_centers = [-1]*numExamples
	for _ in range(maxIterations) :
		iterations += 1
		corr_points = [[] for _ in range(numCentroids)]
		new_corr_centers = []
		# Find closest cluster centers for each point
		for index in range(numExamples) :
			# Euclidean Distance
			diff_mat = np.subtract(centroids_mat, np.array([data_mat[index] for _ in range(numCentroids)]))
			dists = [np.linalg.norm(vec) for vec in diff_mat]
			center = np.argmin(dists)
			new_corr_centers.append(center)
			corr_points[center].append(index)

		# Move cluster center to center of corresponding points
		for index in range(numCentroids) :
			rel_points = data_mat[corr_points[index]].transpose()
			centroids_mat[index] = np.array([np.mean(pt_points) if pt_points.any() else 0 for pt_points in rel_points])

		if new_corr_centers == corr_centers :
			break

		corr_centers = list(new_corr_centers)

	return (centroids_mat, corr_centers)

