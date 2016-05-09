#!/usr/bin/env python
import re
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

	
def imagecheck(img):
	def hascontent(str):
		re_content = re.compile('\w')
		return re_content.match(str)
	def iswhitespace(str):
		re_whitespace = re.compile('^\s*$')
		return re_whitespace.match(str)
		
	#find values and avoid keyerrors if attributes don't exist at all
	alt = img.get('alt','')
	title = img.get('title','')

	#title with only white space carries no significance
	if iswhitespace(title):
		title = ''
	
	print('image: ',img['src'])
	
	if alt or title:
		if iswhitespace(alt) and title == '':
			print('OKAY?: Decorative image')
		elif alt == title:
			print('ATTN!: alt and title should not be the same.')	
		else:
			print('OKAY')
		#vocab check tag content
		if hascontent(alt):
			badwords = spellcheck(alt.split(' '))
			if len(badwords) > 0:
				print('Alt text not in vocab: ',badwords)
		if hascontent(title):
			badwords = spellcheck(title.split(' '))
			if len(badwords) > 0:
				print('Title text not in vocab: ',badwords)
	else:
		print('ATTN!: image must have alt or title content')
		

	

def imagereport(images):
	data = {
		'fname': 'Image report',
		'title': 'Image report',
		'count': len(images),
		'alts': [],
		'titles': [],
	}
	for img in images:
		data['alt'].append(img['alt'])
		data['title'].append(img['title'])
	for img in images:
		if img['alt'] == "":
			img['alt'] = '*** MISSING ALT ***'
		altlst.append(img['alt'])
	return data

# Setup
url = input("enter URL to analyse: ")
page = HTMLPage(url)
for img in page.images:
	imagecheck(img)

print("word count: ",len(page.words))
print("Words not in vocab: \n",spellcheck(page.words))
print("link checking: ",page.linkreport())
# print(word_frequency_report(page.words))


input("press enter to end script.")
