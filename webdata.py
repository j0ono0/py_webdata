#!/usr/bin/env python

import urllib.request
from bs4 import BeautifulSoup
import re

def getKey(item):
	return item[1]

def validated_url(url):
	if url[0:7] != 'http://' and url[0:8] != 'https://':
		url = 'http://' + url
	return url

def loadpage(url):
	url = validated_url(url)
	response = urllib.request.urlopen(url)
	return response.read()

def list_words(page):
	soup = BeautifulSoup(page,'html.parser')
	[tag.extract() for tag in soup(['head','script'])]
	text = re.sub('\W', ' ', soup.get_text(' '))
	text = re.sub(" {1,}", " ", text)
	return text.split(" ")	
	
def unique_words(page):
	wordlst = list_words(page)
	worddict = {}
	for word in wordlst:
		word = word.lower()
		if word in worddict.keys():
			worddict[word] += 1
		else:
			worddict[word] = 1
	print("unique word count: ", len(worddict))
	return worddict

def dict_to_file(data,file_name):
	#convert dict to lsit of tuples and sort
	wordlst = data.items()
	wordlst = sorted(wordlst, key = getKey, reverse = True)
	#output to file
	file = open(file_name, 'w')
	file.write("%s Number of entries: \n" % len(wordlst))
	for entry in wordlst:
		file.write("%s: %s\n" %(entry[1],entry[0]))
	file.close()
	print("data written to: %s" % file_name)

url = input("enter URL to analyse: ")
#scrapepage(url)
page = loadpage(url)
unique_words = unique_words(page)
dict_to_file(unique_words,'unique-words.txt')

input("press enter to end script.")
