#!/usr/bin/python
import util
import numpy as np
import random

np.set_printoptions(formatter={'float': lambda x: '%.2f\t'%round(x,2)})

def getBestBarList(midiFileName):
	barLists = util.getNGramBarList(midiFileName)
	return barLists[0]
	#return best bar list in barLists

# gets a list of euclidean distances between the rows of mat_a and mat_b[index]
def euclideanDistance(mat_a, mat_b, index) :
	diff_mat = np.subtract(mat_a, np.array([mat_b[index] for _ in range(mat_a.shape[0])]))
	dists = [np.linalg.norm(vec) for vec in diff_mat]
	return dists

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
			dists = euclideanDistance(centroids_mat, data_mat, index)
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

def evaluateKmeansClusters(midiFileName, centroids, corr_centers) :
	bestBarList = getBestBarList(midiFileName)
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

