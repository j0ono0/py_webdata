
# Convert owl2-lwl list into a pickled list of just words

import pickle

def pickle_lst():
	with open("vocab.pickle",'wb') as f:
		pickle.dump(wordlst,f)
		print('vocab saved to file')
		
def loadpickle(filename):
	with open(filename,'rb') as f:
		vocab = pickle.load(f)
		return vocab

filename = 'owl2-lwl.txt'
wordlst = []
with open(filename,'r') as f:
	for line in f:
		line = line.lower()
		word = line.split(" ")[0].strip()
		wordlst.append(word)

pickle_lst()
vocab = loadpickle('vocab.pickle')
print(len(vocab))