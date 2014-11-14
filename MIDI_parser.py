from mido import MidiFile
from mido import MetaMessage
import sys
import os

#mid = MidiFile(os.path.join('99-Will_it_Go_Round_in_Circles_(Billy_Preston).mid'), type=2)
if len(sys.argv) == 2:
  mid = MidiFile(os.path.join(sys.argv[1]))
else:
  mid = MidiFile(os.path.join('37-Tighter_Tighter_(Alive).mid'))

ticks_per_beat = mid.ticks_per_beat
tempo = 120

for i, track in enumerate(mid.tracks):
  time = 0
  channels = {}
  print('Track {}: {}'.format(i, track.name))
  
  for message in track:
    if message.type == 'note_on':
      channels[message.channel] = []
  print channels



  for message in track:
    if message.type == 'set_tempo':
      print 'tempo:', message.tempo
      tempo = message.tempo

    seconds_per_beat = tempo / 1000000.0
    seconds_per_tick = seconds_per_beat / float(ticks_per_beat)
    time_in_ticks = time / seconds_per_tick
    time_in_seconds = time_in_ticks * seconds_per_tick
    beats_per_seconds = 1000000 / tempo
    '''
    print 'seconds_per_beat', seconds_per_beat
    print 'seconds_per_tick', seconds_per_tick
    print 'time_in_ticks ', time_in_ticks
    print 'time_in_seconds', time_in_seconds
    print 'beats_per_seconds', beats_per_seconds
    print '\n'
    '''

    if message.type == 'note_on':
      time += message.time * seconds_per_tick
      if message.velocity > 0:
        channels[message.channel].append((time, message.note))

  # add beat lines

  totalTime = int(mid.length)
  num = totalTime * 10 / 3 + 1
  channels[-1] = []
  channels[-1].extend([(j * 3 / 10. - 1e-5, 0) for j in range(num)])
  channels[-1].extend([(j * 3 / 10., 100) for j in range(num)])
  channels[-1].extend([(j * 3 / 10. + 1e-5, 0) for j in range(num)])
  ch = []
  for j in range(num):
    ch.extend([channels[-1][j], channels[-1][num + j], channels[-1][2 * num + j]])
  channels[-1] = ch

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
