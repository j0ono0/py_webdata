#!/usr/bin/env python

import urllib.request
import xml.etree.ElementTree as ET
import time
from bs4 import BeautifulSoup
import re

def weather_adelaide():
	response = urllib.request.urlopen('ftp://ftp2.bom.gov.au/anon/gen/fwo/IDA00100.dat')
	data = response.read().decode(encoding="UTF-8")
	lines = data.split("\n")
	for count, line in enumerate(lines):
		lines[count] = line.split("#")
		if lines[count][0] == "Adelaide":
			adlref = count
	forcasttime = time.strptime(lines[adlref][2],"%Y%m%d")
	forcasttimestr = time.strftime("%d/%m/%y",forcasttime)
	print ("Forecast weather in %s on %s: %s and %s" % (lines[adlref][0],forcasttimestr, lines[adlref][6], lines[adlref][7].lower()))

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

def scrapepage(url):

	def getKey(item):
		return item[1]
		
	response = urllib.request.urlopen(url)
	data = response.read()
	soup = BeautifulSoup(data,'html.parser')
	text = re.sub('\W',' ',soup.get_text())
	text = re.sub(" {2,}", " ", text)
	lst = text.split(" ")
	words = {}
	for word in lst:
		word = word.lower()
		if word in words.keys():
			words[word] += 1
		else:
			words[word] = 1
	print("unique word count: ", len(words))
	wordlst = words.items()
	wordlst = sorted(wordlst, key = getKey, reverse = True)
	
	file = open('page-analysis.txt', 'w')
	file.write("%s different word on the page</br>" % len(wordlst))
	for entry in wordlst:
		file.write("%s: %s\r\n" %(entry[1],entry[0]))
	file.close()
		
print("------------------")
# news_just_in()
print("------------------")
# weather_adelaide()
print("------------------")
url = input("enter URL to analyse: ")
scrapepage(url)
input("press enter to end script.")
