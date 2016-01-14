
import pickle

filename = 'owl2-lwl.txt'
wordlst = []
with open(filename,'r') as f:
	for line in f:
		lst = line.split(" ")
		word = lst[0].lower()
		wordlst.append(word)
print(len(wordlst))

def pickle_lst():
	with open("vocab.pickle",'wb') as f:
		pickle.dump(wordlst,f)
		print('vocab saved to file')
		
def loadpickle(filename):
	with open(filename,'rb') as f:
		vocab = pickle.load(f)
		print(len(vocab))
		print('qi' in vocab)
		
loadpickle('vocab.pickle')