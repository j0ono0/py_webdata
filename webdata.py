#!/usr/bin/env python

import pickle
import os

from HTMLPage import HTMLPage

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

# aid with sorting list of tuples
def getKey(item):
	return item[1]

def word_frequency_report(wordlst):
	worddict = {}
	for word in wordlst:
		word = word.lower()
		if word in worddict.keys():
			worddict[word] += 1
		else:
			worddict[word] = 1
	output = "Total unique word count: %s\r\n" % len(worddict)
	
	#Sort into list from most to least frequent. Return data as a string
	tuplelst = worddict.items()
	tuplelst = sorted(tuplelst, key = getKey, reverse = True)
	for entry in tuplelst:
		output += "%s: %s\n" %(entry[1],entry[0])
	return output

def spellcheck(wordlst):
	with open('vocab.pickle','rb') as f:
		vocab = pickle.load(f)
	notwords = []
	for word in wordlst:
		word = word.lower()
		if word not in vocab:
			notwords.append(word)
	return notwords
	

# Setup
url = input("enter URL to analyse: ")
page = HTMLPage(url)
print("word count: ",len(page.words))
print("Words not in vocab: \n",spellcheck(page.words))
print("link checking: ",page.linkreport())
# print(word_frequency_report(page.words))

input("press enter to end script.")
