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

