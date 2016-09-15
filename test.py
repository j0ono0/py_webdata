#!/usr/bin/env python

from HTMLPage import HTMLPage
from wordsmith import wordsmith
import pprint

url = 'file:///C:/Users/John/Documents/Projects/py_webdata/testsite/page.html'
url2 = 'http://johnnewall.com'
url3 = 'http://www.unisa.edu.au/Study-at-UniSA/'
url4 = 'http://johnnewall.com/articles/case-study-staff-profile-pages/'

page = HTMLPage(url2)           # Page object


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



def test_keyword_density(*tags):
    print("TEST: keyword density\r\n")
    # list keyword frequency in titles
    titles = page.gettext(tags)
    words = ' '.join(titles).split(' ')
    ws = wordsmith(words)
    kw_density = ws.keyword_density()
    for entry in kw_density:
        print(bytes(entry[0], 'utf-8'),':',entry[1])


test_page_vocab()
# test_keyword_density('h1','h2','h3','h4','h5','h6')
# fails to print right single apostrophe
# test_keyword_density('p')
