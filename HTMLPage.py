#!/usr/bin/env python

import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.error import HTTPError
from bs4 import BeautifulSoup

class HTMLPage:
	
	def __init__(self,url):
		self.url = url
		self.soup = self.getsoup(self.url)
		self.links = self.findlinks() 
	
	def getsoup(self,url):
		parts = urlparse(url)
		if(parts[0] != "" and [2] != ""):
			response = urllib.request.urlopen(url)
			return BeautifulSoup(response.read(),'html.parser')
		print("Request failed: URL must include a scheme (eg 'http://', 'https://' or 'file://') and path (eg '/mysite').")
			
	def findlinks(self):
		links = self.soup.find_all('a')
		for i,link in enumerate(links):
			links[i] = urljoin(self.url,link['href']) #convert all links into absolute urls
		return links

	def linkstatus(self,url):
		try:
			response = urllib.request.urlopen(url)
			return True
		except:
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
print(len(page.links))
print(page.linkreport(page.links))

'''----------------------------
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
	-------------------------------------------'''