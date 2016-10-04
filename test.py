#!/usr/bin/env python

from HTMLPage import HTMLPage
from wordsmith import wordsmith
from jinja2 import Environment, FileSystemLoader
import os

url = 'file:///C:/Users/John/Documents/Projects/py_webdata/testsite/page.html'
url2 = 'http://johnnewall.com'
url3 = 'http://www.unisa.edu.au/Study-at-UniSA/'
url4 = 'http://johnnewall.com/articles/case-study-staff-profile-pages/'


def test_page_vocab():
    text = wordsmith(page.gettext())    # Text object
    outvocab = text.invocab(False)
    invocab = text.invocab()
    # convert to bytes for printing to console
    for i,word in enumerate(outvocab):
        outvocab[i] = bytes(word, 'utf-8')
    print("TEST: page vocab\r\n")
    print('%s words not in vocab: \n' % len(outvocab))
    print(outvocab,'\n')
    print('%s words in vocab:\n' % len(invocab))
    print(invocab,'\n')


def keyword_report():
    h1 = wordsmith(page.gettext('h1'))
    print("keyword density: h1")  
    print(h1.keyword_density())
    
    alltext = wordsmith(page.gettext())
    print("keyword density: All text on page")    
    print(alltext.keyword_density())



page = HTMLPage(url)   # Create a page object
imgdata = page.attr_data('img','src','alt','title')
linkdata = page.attr_data('a','content','href','id','class')

env = Environment(loader = FileSystemLoader('templates'))
template = env.get_template('report.html')
fname = 'image-report.html'
context = {
    'imgdata':imgdata,
    'linkdata':linkdata
}
with open(os.path.join('reports',fname),'w') as f:
    f.write(template.render(context))
print('document \'%s\' created.' % fname)

