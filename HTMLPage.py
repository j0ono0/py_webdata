#!/usr/bin/env python

import urllib.request
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.error import URLError
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
        self.images = self.soup.find_all('img')
    
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
                lst += re.sub("[^a-zA-Z0-9]+"," ", tag.string).split(" ")
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
        
    def resource_exists(self,url):
        url = urljoin(self.url, url)
        try:
            res = urllib.request.urlopen(url)
            return True
        except URLError as e:
            pass
        return False
    
    # Collate data relating to a tag
    # arguments include all potential tag attributes plus the following special ones:
    # content: returns the content of the tag
    # validate-src: tests whether the src loads
    # validate-href: tests whether the href loads
    def tag_data(self,tag,*args):
        tags = self.soup.find_all(tag)
        data = {
            'head':[],
            'body':[[] for i in range(len(tags))],
        }
        for i, arg in enumerate(args):
            data['head'].append(arg)
            for j, tag in enumerate(tags):
                if arg == 'content':
                    value = tag.text
                elif arg == 'validate-href':
                    value = '&#x2713;' if self.resource_exists(tag['href']) else '&#x2715;'
                elif arg == 'validate-src':
                    value = '&#x2713;' if self.resource_exists(tag['src']) else '&#x2715;'
                else:
                    value = tag[arg] if tag.has_attr(arg) else ""
                data['body'][j].append(value)
        return data
        
