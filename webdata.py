#!/usr/bin/env python

import urllib.request
from bs4 import BeautifulSoup
import re
import pickle
import os
# my own modules
import linktools as link

# Return HTML page as BeautifulSoup obj
def loadpage(url):
	parts = urlparse(url)
	if(parts[0] != "" and [2] != ""):
		response = urllib.request.urlopen(url)
		return BeautifulSoup(response.read(),'html.parser')
	print("Request failed: URL must include a scheme (eg 'http://', 'https://' or 'file://') and path (eg '/mysite').")


def save_report(text,filename):
	filename += '.txt'
	cwd = os.getcwd()
	dir = os.path.join(cwd,"reports")
	filepath = os.path.join(dir,filename)

	if not os.path.exists(dir):
		os.makedirs(dir)
	with open(filepath,'w') as f:
		f.write(text)
	print('Report created: %s' % filename)
	
def list_words(soup):
# return a list of all words that *display* on the webpage
	[tag.extract() for tag in soup(['head','script'])]
	text = re.sub('\W', ' ', soup.get_text(' '))
	text = re.sub(" {1,}", " ", text)
	return text.split(" ")	
	
# aid with sorting list of tuples
def getKey(item):
	return item[1]

def unique_word_report(soup):
	wordlst = list_words(soup)
	worddict = {}
	output = "Unique word report\n------------------\r\n"

	for word in wordlst:
		word = word.lower()
		if word in worddict.keys():
			worddict[word] += 1
		else:
			worddict[word] = 1
	
	output += "Total unique word count: %s\r\n" % len(worddict)
	
	tuplelst = worddict.items()
	tuplelst = sorted(tuplelst, key = getKey, reverse = True)
	for entry in tuplelst:
		#remove comment to include in output (taken out for convenience whilst developing)
		# output += "%s: %s\n" %(entry[1],entry[0])

	return output
	
def word_count_report(soup):
	words = list_words(soup)
	output = "total word count: %s\n" % len(words)
	return output

def hyperlink_report(soup):

# Setup
url = input("enter URL to analyse: ")
report = "Web page report: %s\n" % url
soup = loadpage(url)

# Assemble word count report & save
report += unique_word_report(soup)
save_report(report,'Report')


input("press enter to end script.")
