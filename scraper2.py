#!/usr/bin/python

# python scraper.py <# files you want to download>

# import modules
import urllib2
import re
import os

def main():
	res = urllib2.urlopen("http://www.free-midi.org/midi/g/green-day/pg4/")
	html = res.read()
	for match in re.findall(r'<a href="(http://www.free-midi.org/song/green.*)" itemprop=', html):
		try :
			res2 = urllib2.urlopen(match)
			html2 = res2.read()
			mid = re.findall(r'<a href="(http://www.free-midi.org/midi1/g/.*\.mid)" on.*>Download</a>', html2)[0]
			os.system("wget %s"%(mid))
		except :
			print "Error"


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()