#!/usr/bin/env python

import urllib.request
import xml.etree.ElementTree as ET

def weather_adelaide():
	response = urllib.request.urlopen('ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat')
	data = response.read().decode(encoding="UTF-8")
	lines = data.split("\n")
	for count, line in enumerate(lines):
		lines[count] = line.split("#")
		if lines[count][0] == "Adelaide":
			adlref = count
	print ("Current weather in %s: %s and %s" % (lines[adlref][0], lines[adlref][6], lines[adlref][7].lower()))

	
def news_just_in():
	response = urllib.request.urlopen('http://www.abc.net.au/news/feed/51120/rss.xml')
	tree = ET.parse(response)
	root = tree.getroot()[0]
	titles = []
	for item in root.iter('item'):
		titles.append(item.find('title').text)

	print('Last 10 news updates from ABC news website:')		
	for i in range(10):
		print('%d: %s' %(i+1,titles[i]))

print("------------------")
news_just_in()
print("------------------")
weather_adelaide()
print("------------------")
input("press enter to end script.")