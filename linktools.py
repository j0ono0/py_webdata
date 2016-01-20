#! user/bin/env python


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
	
def works(url):
# TO DO: Does not ensure bookmark exists on page
	try:
		response = urllib.request.urlopen(url)
		return True
	except:
		Return False
		
def count(soup):
	anchor_types = {'internal':0,'external':0,'bookmarks':0}
	anchors = soup.find_all("a")
	
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
	output = "Number of links on page: %s\n" % (len(anchors))
	


	