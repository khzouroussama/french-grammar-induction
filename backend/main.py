import re
import nltk
import math
# import Corpus 

# path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok.stanford-pos'
path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok copy.stanford-pos'

pos_corpus : list  = []

with open(path2pos_corpus , 'r' , encoding="utf8") as f:
    for line in f :
        txt_list = re.split(r'\s+|[\n]+', line)
        # print(txt_list)
        for word in txt_list : 
            if word != '' :
                *token , pos =  word.split('_') 
                pos_corpus.append(
                    ('_'.join(token) , pos)
                ) 
        

# print(len(pos_corpus) ,)) 
ngram_tagger = nltk.UnigramTagger(train=[pos_corpus] , verbose=True) 



text = 'Bonjour passent sans problèmes'
print(ngram_tagger.tag(text.split()))
