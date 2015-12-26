#!/usr/bin/env python

import urllib.request

response = urllib.request.urlopen('ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat')
data = response.read().decode(encoding="UTF-8")
lines = data.split("\n")
for count, line in enumerate(lines):
	lines[count] = line.split("#")
	if lines[count][0] == "Adelaide":
		adlref = count

print ("current weather in %s: %s and %s" % (lines[adlref][0], lines[adlref][6], lines[adlref][7].lower()))
input("press enter to close window.")