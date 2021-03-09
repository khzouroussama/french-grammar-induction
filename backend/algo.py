import re
import nltk
import math
from sacremoses import MosesTokenizer
from pickle import dump ,load
from operator import itemgetter
from os import system, name 
from nltk import CFG

def loadCorpus(file, delimetre='_') :
    pos_corpus : list  = []

    with open(file , 'r' , encoding="utf8") as f:
        tokens = []
        for sent in re.split(r'\n+', f.read()) :
            proceced_sent = []
            for word in re.split(r'\s+', sent) :
                if word != '' :
                    *token , pos = word.split(delimetre)
                    proceced_sent.append(
                        ('_'.join(token) , pos)
                    )
            if len(proceced_sent) :
                pos_corpus.append(proceced_sent) 

    return pos_corpus


def getPOSSentencesFromText(text, tagger, sent_tokenizer, tokenizer) :
    # escape ruins abstraction
    return [tagger.tag(sentence) for sentence in sent_tokenizer(tokenizer(text ,escape=False))]


def saveTagger(outputFile,tagger) :
    output = open(outputFile, 'wb')
    dump(tagger, output, -1)
    output.close()

def importTagger(inputfile) :
    input = open(inputfile, 'rb')
    tagger = load(input)
    input.close()
    return tagger


def trainTagger(pos_tagged):
    size = int(len(pos_tagged) * 0.9)
    train_sents = pos_tagged[:size]
    test_sents = pos_tagged[size:]

    tagger = nltk.UnigramTagger(train=pos_tagged, verbose=True ,backoff=nltk.DefaultTagger('None') )
    tagger = nltk.BigramTagger(train=pos_tagged, verbose=True,backoff=tagger)
    tagger = nltk.NgramTagger(3,train=pos_tagged, verbose=True,backoff=tagger)
    tagger = nltk.NgramTagger(4,train=pos_tagged, verbose=True,backoff=tagger)
    print('(train={} , test={} , evaluate={})'.format(size ,len(pos_tagged)-size ,tagger.evaluate(test_sents)))

    return tagger
    
def getAllTags(pos_tagged):
    return set([word[1] for sent in pos_tagged for word in sent ])


def importCFG(filename):
    with open(filename , 'r' , encoding="utf8") as f:
        return f.read()

def saveCFG(filename , CFG):
    with open(filename , 'w' , encoding="utf8") as f:
        f.write(CFG)

##########################################
#  IMPLEMENTING SELAB_GUESSOUM THE ALGORITHM
##########################################

def NGramExtraction(pos_tagged) : 
    ngrams = []
    for sent in pos_tagged :
        for i in range(2 , len(sent) + 1) :
            ngrams.extend(nltk.ngrams(map(lambda x : x[1] ,sent),i))
    return ngrams
   
def substitution(pos_tagged , R , non_terminal) :
    result = []
    for sen in pos_tagged : 
        for i in range(len(sen) - len(R)+1) :
            if tuple(map(lambda x:x[1],sen[i:i + len(R)])) == R :
                sen = sen[:i]+[(non_terminal,non_terminal)]+sen[i + len(R):]
        result.append(sen)
    return result

def printProgress(maxProgress , pos_tagged , R) :
    max=50
    prog = max - int(((sum(len(s) for s in pos_tagged) - len(pos_tagged) + 1) / maxProgress) * max)
    min = max - int(((maxProgress - len(pos_tagged) + 1) / maxProgress ) * max)
    # normelize PROGRESS
    prog = int(((prog - min)/(max - min))*50)
    system('clear')
    print('Building Grammar :')
    print('\nCurrent rule : \n\t#R'+str(len(R)-1) ,'->' ,' '.join(R[len(R)-1]))
    print('\n[{}] {}%'.format('='*(prog)+' '*(max-prog) , int(((prog) / max)*100)) )

def printGrammar(R):
    print('Grammar :' , type(R))
    for (idx ,val) in enumerate(R) :
        print('#R'+str(idx) ,'->' ,' '.join( val))

def FormatGrammarAsCFG(R):
    return 'S -> '+ ' | '.join(['R'+str(i) for i in range(len(R))])+'\n' + '\n'.join([
        'R'+str(len(R) - idx - 1) +' -> '+' '.join([r.replace('#','') if r.startswith('#') else '"'+r+'"' for r in val])
        for (idx,val) in enumerate(reversed(R))
    ])

def InductGrammar(pos_tagged) :
    i = 0
    R = []
    maxProgress = sum(len(s) for s in pos_tagged)
    while sum(len(s) for s in pos_tagged) != len(pos_tagged) : 
        freq = nltk.FreqDist(sorted(NGramExtraction(pos_tagged), key=len, reverse=True))
        R.append(freq.max())
        printProgress(maxProgress, pos_tagged, R)
        pos_tagged = substitution(pos_tagged, freq.max(), '#R'+str(i))
        i += 1
    return R

def parse(sent ,grammar):
    #Returns nltk.Tree.Tree format output
    a = []  
    parser = nltk.ChartParser(grammar)
    for tree in parser.parse(sent):
        a.append(tree)
    if(len(a) != 0) :
        return(a[0]) 
    return None


if __name__ == "__main__" :
    # 
    # path2pos_corpus = 'data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok.stanford-pos'
    # path2pos_corpus = 'data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok copy.stanford-pos'
    # path2pos_corpus = 'data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok copy 2.stanford-pos'

    sent_detector = nltk.data.load('tokenizers/punkt/french.pickle') 


    # moses = MosesTokenizer(lang='fr')
    # print(getPOSSentencesFromText(text, unigram_tagger,sent_detector.sentences_from_tokens, moses.tokenize))


    # pos_tagged = loadCorpus(path2pos_corpus)

    # saveCFG('models/french_CFG.txt',FormatGrammarAsCFG(InductGrammar(pos_tagged)))
    # importCFG('models/french_CFG.txt')
    # print(getAllTags(pos_tagged))

    # freq = nltk.FreqDist(NGramExtraction(pos_tagged))
    # print(sorted(freq.items(), key=itemgetter(1), reverse=True)[:10])


    moses = MosesTokenizer(lang='fr')
    # # train tagger 
    # unigram_tagger  = trainTagger(pos_tagged)
    # save tagger
    # saveTagger('models/unigram_tagger.pkl', unigram_tagger)
    # import tagger
    unigram_tagger = importTagger('models/unigram_tagger.pkl')

    # print(unigram_tagger.tag(moses.tokenize(sent)))

    sent = u"Il avait participé, à un rang subalterne, à la création de l'aviation israélienne et pris part aux combats aériens durant la guerre de 1948."
    # sent = u""
    # sent = u""

    tagged_sent = [token[1] for token in unigram_tagger.tag(moses.tokenize(sent ,escape=False))]

    grammar_str = importCFG('models/french_CFG.txt')

    grammar = CFG.fromstring(grammar_str.split('\n'))
    # print(grammar.productions())

    # rd_parser = nltk.RecursiveDescentParser(grammar)

    # print(tagged_sent)
    # print(grammar)

    # print parsing
    # parsing kinda working , SLOOWWW :'( THERDET



    #Gives output as structured tree   
    print(parse(tagged_sent)) 

    #Gives tree diagrem in tkinter window
    parse(tagged_sent).draw()

