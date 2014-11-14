#!/usr/bin/python

# python scraper.py <# files you want to download>

# import modules
import sys
import urllib2
import re
import os

def main():
	num = 0
	sent = False
	for i in range(1, 79) :
		response = urllib2.urlopen('http://www.midiworld.com/search/%s/?q=rock'%i)
		html = response.read()
		for match in re.findall(r'([A-Z].*) - <a href="(.*)" target.*>download</a>', html) :
			print "Downloading midi file: %s"%match[0]
			os.system('wget %s --output-document=\"%s-%s.mid\"'%(match[1], num, match[0].replace(" ","_")))
			print '-'*20
			num += 1
			if len(sys.argv) >= 2 and num >= int(sys.argv[1]) :
				sent = True
				break
		if sent :
			break




# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()