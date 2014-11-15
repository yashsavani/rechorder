#!/usr/bin/python

from mido import MidiFile
from mido import MetaMessage
import math
import sys
import os
from cluster import KMeansClustering
import random

BEATS_PER_CHUNK = 4


seenFeatures = []

def plotBeat(data): # data = (note, velocity) list
  ret = [0] * 12
  for note, velocity in data:
    ret[note % 12] += velocity
  return ret


if len(sys.argv) == 2:
  mid = MidiFile(os.path.join(sys.argv[1])) # create Mido object
else:
  mid = MidiFile(os.path.join('37-Tighter_Tighter_(Alive).mid'))

ticks_per_beat = mid.ticks_per_beat
tempo = 120

for i, track in enumerate(mid.tracks): # go through all tracks
  time = 0
  channels = {}
  print('Track {}: {}'.format(i, track.name))

  for message in track:
    if message.type == 'note_on': # turn a note on
      channels[message.channel] = []
  print channels

  if len(channels) == 0:
    continue
  
  messages = []
  beats = []
  chunks = []

  prevBeat = None

  for message in track:
    if message.type == 'set_tempo':
      print 'tempo:', message.tempo
      tempo = message.tempo

    seconds_per_beat = tempo / 1000000.0
    seconds_per_tick = seconds_per_beat / float(ticks_per_beat)
    time_in_ticks = time / seconds_per_tick
    time_in_seconds = time_in_ticks * seconds_per_tick
    beats_per_seconds = 1000000 / tempo

    if message.type == 'note_on':
      beat = math.floor(time / seconds_per_beat)
      if beat != prevBeat:
        beats.append(messages)
        chunks.append((time, [(x.note, x.velocity) for y in beats[-BEATS_PER_CHUNK:] for x in y]))
        messages = []
        prevBeat = beat
      
      messages.append(message)

      time += message.time * seconds_per_tick
      if message.velocity > 0:
        channels[message.channel].append((time, message.note))

  if len(messages) > 0:
    beats.append(messages)
  chunks.append((time, [(x.note, x.velocity) for y in beats[-BEATS_PER_CHUNK:] for x in y]))

  # add beat lines

  totalTime = int(mid.length)
  num = totalTime * 10 / 3 + 1
  '''
  channels[-1] = []
  channels[-1].extend([(j * 3 / 10. - 1e-5, 0) for j in range(num)])
  channels[-1].extend([(j * 3 / 10., 100) for j in range(num)])
  channels[-1].extend([(j * 3 / 10. + 1e-5, 0) for j in range(num)])
  ch = []
  for j in range(num):
    ch.extend([channels[-1][j], channels[-1][num + j], channels[-1][2 * num + j]])
  channels[-1] = ch
  '''

  #print chunks

  def innerProduct(x, y):
    return sum(a * b for a, b in zip(x, y))
  for i in range(len(chunks)):
    chunks[i] = (chunks[i][0], chunks[i][1], plotBeat(chunks[i][1])) # add feature vectors to chunks
  #chunks = chunks[:10]
  #print chunks

  # run k-means


  possibleFeatures = set(tuple(x[2]) for x in chunks) # unique feature vectors
  
  NUM_CLUSTERS = min(7, len(possibleFeatures))
  print 'Track %s -- Performing %d-means clustering on %d chunks of %d beats' % (track.name, NUM_CLUSTERS, len(chunks), BEATS_PER_CHUNK)

  centroids = random.sample(possibleFeatures, NUM_CLUSTERS)
  assignment = [0] * len(chunks)

  for t in range(30):
    for i, (time, chunk, phi) in enumerate(chunks):
      def dist(centroid):
        return sum((a - b) ** 2 for a, b in zip(centroid, phi)) ** 0.5
      minIndex, minCentroid = min([(k, centroid) for k, centroid in enumerate(centroids)], key=lambda x: dist(x[1]))
      assignment[i] = minIndex

    for k in range(len(centroids)):
      phiAssignedToK = [phi for i, (time, chunk, phi) in enumerate(chunks) if i == k]
      if len(phiAssignedToK) == 0: # centroid died out
        centroids[k] = random.sample(possibleFeatures)
        continue
      averagePhi = [0] * len(phiAssignedToK[0]) # assume at least one assigned to this centroid
      for phi in phiAssignedToK:
        for j, p in enumerate(phi):
          averagePhi[j] += p
      for j in range(len(averagePhi)):
        averagePhi[j] /= 0. + len(phiAssignedToK)
      #print averagePhi
        
      centroids[k] = [phi / (0. + len(averagePhi)) for phi in averagePhi]
    
  channels[-2] = []
  for i, c in enumerate(chunks):
    if i > 0:
      channels[-2].append((c[0], previousLabel))
    previousLabel = assignment[i] * 100. / NUM_CLUSTERS
    channels[-2].append((c[0], previousLabel))

    
  '''
  kMeans = KMeansClustering(chunks, lambda x, y: innerProduct(x[2], y[2]))
  cluster = kMeans.getclusters(3)
  for c in cluster:
    print c
  print cluster
  '''
  

  # write to file
  
  g = open('track' + str(i) + '.m', 'w')
  g.write('channels = {')

  for c in channels:
    g.write('{')
    for note in channels[c]:
      g.write('{%f, %d},' % note)
    g.write('},\n')

  g.write('};\n')
  g.write('ListLinePlot[channels, ImageSize -> 17000, AspectRatio -> 0.05, PlotRange -> {0, 100}]')
  g.close()

print 'ticks per beat:', mid.ticks_per_beat
print 'song length:', mid.length
