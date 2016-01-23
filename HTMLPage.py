#!/usr/bin/env python

import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup

class HTMLPage:
	
	def __init__(self,url):
		self.url = url
		self.soup = self.load(url)
		self.links = self.findlinks(self.soup) 
	
	def load(self,url,returnsoup = True):
		try:
			response = urllib.request.urlopen(url)
			if returnsoup == True:
				return BeautifulSoup(response.read(),'html.parser')
			else:
				return response.read()
		except:
			return None
				
	def makesoup(self,page):
		if page == None:
			return None
		return BeautifulSoup(page,'html.parser')
			
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
			
	def linkreport(self,links):
		report = {'on':0,'off':0}
		for link in links:
			if self.linkstatus(link):
				report['on'] += 1
			else:
				report['off'] += 1
		return report
	
# testing
page = HTMLPage('file:///C:/Users/John/Documents/Projects/py_webdata/testsite/page.html')
print("link count: ",len(page.links))
print("link status: ",page.linkreport(page.links))
