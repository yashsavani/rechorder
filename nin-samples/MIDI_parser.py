from mido import MidiFile
import os
for message in MidiFile('nine_inch_nails-hurt.mid').play():
	print type(message)