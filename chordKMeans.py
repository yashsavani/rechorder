#!/usr/bin/python
import util
import numpy as np
import random

np.set_printoptions(formatter={'float': lambda x: str(x)+ '\t'})

def getBestBarList(midiFileName):
	barLists = util.getNGramBarList(midiFileName)
	#return best bar list in barLists

def getFeatureCentroids(midiFileName, numCentroids=12, maxIterations=100): # basically k-means
	bestBarList = getBestBarList(midiFileName)

	# parse bars into a data matrix
	data_mat = np.array([bar.getKMeansFeatures() for bar in bestBarList]).transpose()

	# initialize the k clusters from k randomly chosen points in the data
	indices = range(data_mat.shape[1])
	random.shuffle(indices)
	centroids_mat = data_mat[:,indices[:numCentroids]]

	iterations = 0
	corr_centers = [-1]*data_mat.shape[1]
	for _ in maxIterations :
		iterations += 1
		corr_points = [[] for _ in range(centroids_mat.shape[1])]
		new_corr_centers = []
		# Find closest cluster centers for each point
		for index in range(data_mat.shape[1]) :
			diff_mat = np.subtract(centroids_mat, np.array([data_mat[:,index] for _ in range(centroids_mat.shape[1])]).transpose()).transpose()
			dists = [np.linalg.norm(vec) for vec in diff_mat]
			center = np.argmin(dists)
			new_corr_centers.append(center)
			corr_points[center].append(index)

		# Move cluster center to center of corresponding points
		for index in range(centroids_mat.shape[1]) :
			rel_points = data_mat[:,corr_points[index]]
			centroids_mat[:,index] = np.array([np.mean(pt_points) for pt_points in rel_points])

		if new_corr_centers == corr_centers :
			break

		corr_centers = list(new_corr_centers)

	return corr_centers


