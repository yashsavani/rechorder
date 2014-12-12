#!/usr/bin/python
import numpy as np
import mido
import itertools
import math
import sys
#np.set_printoptions(formatter={'float': lambda x: str(x)+ '\t'})

NUM_FEATURES = 12

NUM_NOTES = 128

segmentedBeatsMidiFileCache = {}

# IMPORTANT: we assume the midi file has only one track!
#   (ie, it is in format 0)
# This must hold for us to be able to analyze the entire group of instruments
#   at once. Things get a little more complicated if it has more than one track.
def getNGramBarList(midiFileName, n=4): # n = 4 for four lists
  if midiFileName in segmentedBeatsMidiFileCache:
    midi = segmentedBeatsMidiFileCache[midiFileName]
  else:
    segmentedBeatsMidiFileCache[midiFileName] = SegmentedBeatsMidiFile(midiFileName)
    midi = segmentedBeatsMidiFileCache[midiFileName]
  assert(midi.getNumTracks() == 1)
  return [midi.segmentIntoBars(barWidth=n, start=i) for i in range(n)]

# We assume that the midi file only sets its tempo once at the start of the file
#   (which I assume is the case >95% of the time).
# We also assume (IMPORTANT) that the number of tracks, including the header
#   track, is 1. This means that all the instruments are in the same track.
#
# ie, the midi file should be in format 0.
# If your midi file is in format 1 or 2, you can try to find a converter online.
class SegmentedBeatsMidiFile(mido.MidiFile):

  def __init__(self, fileName):
    mido.MidiFile.__init__(self, fileName)
    assert(self.getNumTracks() == 1)
    self.initDefaults()
    self.loadMessages()
    self.initHeaderInfo()
    self.segmentIntoBeats()

  def initDefaults(self):
    self.tempo = 500000

  # Doesn't load control_change or other messages yet.
  # Only works with note_on messages, which is all we really need it to work for.
  def loadMessages(self):
    self.headerMessages = [message for track in self.tracks for message in track \
        if isinstance(message, mido.MetaMessage)]
    self.mainMessages = [message for track in self.tracks for message in track\
        if message.type == 'note_on' and \
        not isinstance(message, mido.MetaMessage)]

  # Right now this only sets tempo because I think it's the only property
  #   that matters.
  def initHeaderInfo(self):
    for message in self.headerMessages:
      if message.type == 'set_tempo':
        self.tempo = message.tempo # microseconds per beat
        self.beatsPerSecond = 1000000. / self.tempo

  def segmentIntoBeats(self):
    self.beats = []
    messages = self.mainMessages

    on = {} # A dict mapping from note : state.
            # A state is a tuple (isOn, length) that
            # tells whether note is currently on, and
            # for how long it was turned on in the
            # current beat, in ticks. isOn is a boolean.

    index = 0
    tickLimit = 0 # Represents how many ticks you have left.
                  # Each message m "consumes" m.time ticks.

    result = []

    # for each beat, do:
    for i in xrange(self.getTotalBeats()):

      # advance to next beat
      tickLimit += self.ticks_per_beat
      # iterate through all messages that can fit into these ticks
      while index < len(self.mainMessages) and \
          tickLimit - self.mainMessages[index].time >= 0:
        message = self.mainMessages[index]
        # add to total time being "on"
        for note in on:
          if(on[note][0]):
            on[note] = (True, on[note][1] + min(self.ticks_per_beat, message.time))

        if message.velocity == 0: # turn the note off
          if message.note in on:
            on[message.note] = (False, on[message.note][1])
        else: # turn the note on
          if message.note in on:
            on[message.note] = (True, on[message.note][1])
          else:
            on[message.note] = (True, 0)

        # consume this many ticks
        tickLimit -= message.time
        index += 1

      # add to total time "on" for the rest of the beat
      for note in on:
        if(on[note][0]):
          on[note] = (True, on[note][1] + tickLimit)

      # Make a deep copy of on, doing some postprocessing:
      #  - Remove notes that are played for 0 ticks
      #  - Remove the (useless) first value of the tuple
      #  - Take the fraction of the length over the ticks per beat
      
      result.append([(note, length / float(self.ticks_per_beat)) \
          for note, (isOn, length) in on.items() if length > 0])
      
      # Take out everything in on that's False
      # and reset everything that's True to 0
      toRemove = []
      for note in on:
        if(on[note][0]):
          on[note] = (True, 0)
        else:
          toRemove.append(note)
      for note in toRemove:
        del on[note]
    self.beats = result

  def getTotalBeats(self):
    if not hasattr(self, 'numBeats'):
      self.numBeats = int(math.floor(self.beatsPerSecond * self.length + 1e-5))
    return self.numBeats

  def getTotalTicks(self):
    return self.ticks_per_beat * self.getTotalBeats()

  def getNumTracks(self):
    return len(self.tracks)

  # Assumes self.beats has already been calculated by
  # self.segmentIntoBeats(). Joins those beats
  # starting at the given index, with the given bar width.
  def segmentIntoBars(self, barWidth=4, start=0):
    assert(start < barWidth)
    beats = ([None] * start) + self.beats
    numBars = (len(beats) + barWidth - 1) // barWidth
    bars = [0] * numBars
    for i in xrange(numBars):
      arr = []
      for j in range(barWidth):
        index = i * barWidth + j
        if index < len(beats) and beats[index] is not None:
          arr.append(beats[index])
      bars[i] = Bar(list(arr), barWidth=barWidth)
    return bars


# A Bar -- a list of beats
class Bar:

  def __init__(self, beats, barWidth=4):
    self.beats = beats
    for i, beat in enumerate(self.beats):
      for j, (note, length) in enumerate(beat):
        self.beats[i][j] = (note, min(length, 1))

  def __str__(self):
    return str(self.beats)

  def __repr__(self):
    return str(self.beats)


  def getKMeansFeatures(self):
    v = [0] * NUM_FEATURES
    for beat in self.beats:
      for note, length in beat:
        v[note % NUM_FEATURES] += length
    return np.array(v)
    
  # Doesn't work yet because velocity information is lost.
  # Need to modify the "on" dict in segmentIntoBeats().
  # Will do this later.
  # Just pick a random one out of the four lists for now.
  def getBarConfidenceFeatures(self):
    if len(self.beats) == self.barWidth and self.beats[0]:
      return 0 # sum(x for x in self.beats[0])
    return 0
    
 
