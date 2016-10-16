#!/usr/bin/env python
# wordsmith module
# spellchecking and the likes...

import pickle

class wordsmith:

    def __init__(self,wordlst):
        self.wordlst = wordlst
        self.vocab = self.loadpickle('vocab.pickle')
        
    
    def loadpickle(self,filename):
        with open(filename,'rb') as f:
            return pickle.load(f)
    
    # Determine if a string represents a number
    def isnumber(self,string):
        try:
            float(string)
        except ValueError:
            return False
        return True
    
    # match words from self.wordlst to words in self.vocab 
    # Defaults to returning positive matches. Setting arg to False returns words not in vocab
    # the latter may indicate a misspelt word
    def invocab(self,validate=True):
        words = []
        for word in self.wordlst:
            word = word.lower()
            if (word in self.vocab) == validate:
                # filter out duplicated and empty entries and numbers
                if word not in words and not self.isnumber(word) and word != '':
                    words.append(word)
        return words
        
    def keyword_density(self):
    # List all repeated words and their frequency
        # Help sorting dicts converted to tuples by keys
        def getkey(item):
            return item[0]
    
        keywords = {}
        for word in self.wordlst:
            word = word.lower()
            if word in keywords.keys():
                keywords[word] += 1
            else:
                keywords[word] = 1
        keywordlst = []
        for key in keywords:
            keywordlst.append([keywords[key],key])
        keywordlst = sorted(keywordlst, key = getkey, reverse = True)
        return keywordlst
         
    