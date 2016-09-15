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
            print("HTMLpage load function failed")
            return None
 
    def findlinks(self,soup):
        links = soup.find_all('a')
        for i,link in enumerate(links):
            links[i] = urljoin(self.url,link['href']) #convert all links into absolute urls
        return links

    def linkstatus(self,url):
        soup = self.load(url)
        if soup:
            frag = urlparse(url)[5]
            if frag == '' or soup.find(id = frag) or soup.find(name = frag):
                return True
        return False
        
    # custom filter for 'gettext' function to find visible text on the page
    def visibletext(self, tag):
        no_content_tags = ['style', 'script', '[document]', 'head', 'title']
        if tag.string is None or tag.name in no_content_tags:
            return False
        return True
    
    # TO DO: DRY the function. 
    # NLTK = dedicated python module, probably a better way to tonkenize the strings to words!
    def gettext(self, *args):
        lst = [] 
        if len(args) is 0:
        # Return all text that diplays on the page
            tags = self.soup.findAll(self.visibletext)
            for tag in tags:
                lst += re.sub("[^\w]"," ", tag.string).split(" ")
            return lst
        else:
        # Return text from requested tags
            for tag in args:
                for tagsoup in self.soup.find_all(tag):
                    for string in tagsoup.stripped_strings:
                        lst += string.split(' ')                        
            return lst
            
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
    
