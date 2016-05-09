#!/usr/bin/env python

import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import re

''' 
TO DO:
* multi threading for loading pages
* request gzip pages from server to save download size
'''
class HTMLPage:
	
	def __init__(self,url):
		self.url = url
		self.soup = self.load(url)
		self.links = self.findlinks(self.soup)
		self.words = self.listwords(self.soup)
		self.images = self.findimages(self.soup)
	
	def load(self,url,returnsoup = True):
		try:
			response = urllib.request.urlopen(url)
			# Ensure B'soup is only give html pages
			if returnsoup == True and'text/html' in response.info()['Content-type']:
				return BeautifulSoup(response.read(),'html.parser')
			else:
				return response.read()
		except:
			return None
			
	def findlinks(self,soup):
		links = soup.find_all('a')
		for i,link in enumerate(links):
			links[i] = urljoin(self.url,link['href']) #convert all links into absolute urls
		return links

	def linkstatus(self,url):
		# urlparse scheme='http', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment=''
		soup = self.load(url)
		if soup:
			frag = urlparse(url)[5]
			if frag == '' or soup.find(id = frag) or soup.find(name = frag):
				return True
		return False
	
	def listwords(self,soup):
	# return a list of all words that *display* on the webpage
		[tag.extract() for tag in soup(['head','script'])]
		text = re.sub('\W', ' ', soup.get_text(' '))
		text = re.sub(" {1,}", " ", text)
		return text.split(" ")	
		
	def linkreport(self):
		report = {'on':0,'off':0}
		for link in self.links:
			if self.linkstatus(link):
				report['on'] += 1
			else:
				report['off'] += 1
		return report
	
	def findimages(self,soup):
		imglst = []
		return soup.find_all('img')
	
