Rechorder
==========

Using artificial intelligence with machine learning to predict the next music motif in a real time MIDI playback.

Visualize a MIDI file on a Mac with:

python visualize.py < Path to MIDI file >

To run the motif silhouette visualizer run the following command:
python motif_sil.py samples/*/*



To run the unsupervised learning algorithm to save the .mtf file that is used in the cross validation test program run the following command
python motif.py < name of file you want to save > samples/*/*

You can run k-fold cross validation with:

python kFoldXValidation.py < path to saved motif file > samples/*/*







Sample usage:

Run the following in command line: (we assume there are 60 MIDI files in sixty_samples/all/)

python motif.py centroid_60_4beats samples/sixty_samples/all/*
python kFoldXValidation.py centroid_60_4beats.mtf samples/sixty_samples/all/*

This prints out ConfusionMatrix: <some big list of matrices>. Copy that value, and run the following in the python  interpreter to show confusion matrices.

python
import matplotlib.pylab as plt
#copy and paste the value of the list of confusion matrices, which is printed at the end if you run the commented code
c = [[[386, 44, 0, 0, 85, 98, 39, 0], [31, 483, 0, 93, 23, 173, 79, 0], [0, 0, 181, 1, 0, 0, 0, 0], [2, 79, 0, 352, 84, 10, 33, 0], [105, 11, 0, 83, 388, 19, 38, 0], [79, 140, 0, 9, 17, 617, 71, 0], [43, 75, 0, 31, 54, 78, 708, 0]], [[427, 40, 1, 3, 54, 74, 47, 56], [48, 528, 1, 57, 20, 165, 55, 8], [0, 0, 178, 0, 1, 0, 0, 3], [5, 47, 0, 369, 72, 20, 37, 10], [49, 19, 0, 57, 441, 26, 42, 10], [89, 157, 0, 13, 11, 577, 70, 16], [70, 77, 3, 42, 46, 76, 666, 9]], [[447, 43, 0, 2, 86, 118, 46, 10], [51, 443, 1, 90, 30, 204, 63, 0], [1, 0, 180, 0, 0, 0, 1, 0], [5, 92, 0, 330, 88, 15, 30, 0], [80, 16, 0, 92, 386, 29, 41, 0], [113, 218, 0, 14, 12, 505, 71, 0], [55, 70, 1, 32, 42, 62, 727, 0]]]

b = [[[value * 1.0 / (sum(row)) for value in row] for row in matrix] for matrix in c]

for index, approach in enumerate(["SVM", "Matching", "Repeat"]):
plt.matshow(b[index])
plt.hold(True)
for i, row in enumerate(c[index]):
for j, count in enumerate(row): 
if count > 0:
plt.text(j-.2, i+.2, count, fontsize = 14)
plt.show()
plt.hold(False)