from mido import MidiFile
import os
for message in MidiFile(os.path.join('samples', 'nin-samples', 'nine_inch_nails-hurt.mid')).play():
	print message