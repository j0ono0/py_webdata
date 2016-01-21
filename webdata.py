#!/usr/bin/env python

# this is the working version!

import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re
import pickle
import os

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

	
def total_word_count(soup):
	return
	
def list_words(soup):
# return a list of all words that *display* on the webpage
	[tag.extract() for tag in soup(['head','script'])]
	text = re.sub('\W', ' ', soup.get_text(' '))
	text = re.sub(" {1,}", " ", text)
	return text.split(" ")	
	
# aid with sorting list of tuples
def getKey(item):
	return item[1]

def word_frequency_report(soup):
	wordlst = list_words(soup)
	worddict = {}

	for word in wordlst:
		word = word.lower()
		if word in worddict.keys():
			worddict[word] += 1
		else:
			worddict[word] = 1
	
	output = "Total unique word count: %s\r\n" % len(worddict)
	
	tuplelst = worddict.items()
	tuplelst = sorted(tuplelst, key = getKey, reverse = True)
	for entry in tuplelst:
		output += "%s: %s\n" %(entry[1],entry[0])

	return output
def word_count_report(soup):
	words = list_words(soup)
	output = "total word count: %s\n" % len(words)
	return output
def hyperlink_report(soup):
	# urlparse scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment=''
	def is_internallink(url,href):
		url = urlparse(url)
		href = urlparse(href)
		if (href[1] == ""):
			return True
		elif(href[1] == url[1]):
			return True
		return False
		
	def is_bookmark(url,href):
	# Link to id or named anchor on same page
		url = urlparse(url)
		href = urlparse(href)
		if (href[0]=="" and href[1]=="" and href[2]=="" and href[3]=="" and href[4]=="" and href[5]!=""):
			return True
		elif(href[0]==url[0] and href[1]==url[1] and href[2]==url[2] and href[3]==url[3] and href[4]==url[4] and href[5]!=""):
			return True
		return False
		
	def link_exists(url):
	# Does not ensure bookmark exists on page
		try:
			response = urllib.request.urlopen(url)
			print("Win: ",url)
		except:
			print("Fail: ",url)
	
	anchor_types = {'internal':0,'external':0,'bookmarks':0}
	anchors = soup.find_all("a")
	output = "Number of links on page: %s\n" % (len(anchors))
	for anchor in anchors:
		href = urljoin(url,anchor['href']) #extract href and convert into absolute path
		link_exists(href)
		if(is_bookmark(url,href)):
			anchor_types['bookmarks'] += 1
		elif(is_internallink(url,href)):
			anchor_types['internal'] += 1
		else:
			anchor_types['external'] += 1

	print(anchor_types)
	return output

	
# Setup
url = input("enter URL to analyse: ")
report = "Web page report: %s\r\n" % url
soup = loadpage(url)
if soup:
	# Assemble word count report & save
	report += hyperlink_report(soup)
	report += word_count_report(soup)
	report += word_frequency_report(soup)
	save_report(report,'Report')


input("press enter to end script.")
