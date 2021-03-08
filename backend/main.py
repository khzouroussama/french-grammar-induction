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


text = """Il faut vraiment clarifier cette affaire et faire connaître ce règlement si particulier qui n'a pas cours ailleurs, peut-être le faire interdire par Bruxelles dont les Canaries bénéficient grandement pour ses infrastructures.
L'acteur Seth MacFarlane a fait l'annonce des nominations pour les Oscars en compagnie de la coanimatrice Emma Watson
C'est ce jeudi qu'on été dévoilées les nominations pour les Oscars, un des plus prestigieux prix remis dans le domaine cinématographique.
Les films Lincoln de Steven Spielberg, Happiness Therapy de David Russel et Amour de Micheal Haneke ont ont fait bonne figure lors de la conférence de presse qui dévoilait ceux qui vont compétitionner pour un prix lors de la présentation du gala le 24 février 2012.
Au total des nominations, Lincoln en reçoit 12 et Life of Pi de Ang Lee en récolte 11.
Les nommés ont été présentés par les animateurs de la soirée très attendue Seth McFarlane et Emma Stone.
Daniel Day Lewis, Denzell Washington, Hugh Jackman, Bradley Cooper et Joaquin Phoenix ont reçu l'honneur de figurer parmi les candidats pour l'Oscar du meilleur acteur.
Naomi Watts, Jessica Chastain, Jennifer Lawrence, Emmanuelle Riva et Quvenzhané Wallis sont de leur côté proposées comme meilleure actrice.
Fait intéressant, Emmanuelle Riva est l'actrice la plus âgée de l'histoire à recevoir cet honneur dans cette catégorie alors que Quvenzhané Wallis est de son côté la plus jeune à recevoir cette nomination
Dans la catégorie du meilleur film, neuf longs métrages ont été sélectionnés: Beasts of the Southern Wild, Happiness Therapy, Zero Dark Thirthy, Lincoln, Les Misérables, Life of Pi, Amour, Django Unchained et Argo.
Voici la liste des nominations pour la 3e cérémonie des Magritte, présidée par Yolande Moreau et présentée par Fabrizio Rongione, qui se tiendra le 2 février 2013.
Jean Charest lors de la dernière campagne électorale québécoise
Le premier ministre défait aux dernières élections générales Jean Charest a annoncé qu'il se joindrait au cabinet d'avocat McCarthy Tétrault pour revenir à la pratique du droit, profession qu'il avait quittée en 1984 pour représenter la circonscription fédérale de Sherbrooke pour les progressistes-conservateurs.
L'ancien chef du Parti Libéral du Québec et ex-vice-premier ministre du Canada a démissionné en septembre 2012 suite à la défaite de son parti aux mains du Parti Québécois aux élections du 4 septembre.
Il a dirigé le Québec pendant les neuf années précédentes.
Son nouveau cabinet a souligné que Jean Charest apporte une expertise inestimable aux clients du cabinet grâce à sa vaste expérience des affaires publiques et sa connaissance approfondie des questions commerciales, économiques et internationales.
Jean Charest sera basé à Montréal et travaillera avec les clients internationaux du bureau d'avocat."""



# 
# path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok.stanford-pos'
path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok copy.stanford-pos'
# path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok copy 2.stanford-pos'

sent_detector = nltk.data.load('tokenizers/punkt/french.pickle') 


# moses = MosesTokenizer(lang='fr')
# print(getPOSSentencesFromText(text, unigram_tagger,sent_detector.sentences_from_tokens, moses.tokenize))


pos_tagged = loadCorpus(path2pos_corpus)

# saveCFG('backend/models/french_CFG.txt',FormatGrammarAsCFG(InductGrammar(pos_tagged)))
# importCFG('backend/models/french_CFG.txt')
# print(getAllTags(pos_tagged))

# freq = nltk.FreqDist(NGramExtraction(pos_tagged))
# print(sorted(freq.items(), key=itemgetter(1), reverse=True)[:10])


moses = MosesTokenizer(lang='fr')
# # train tagger 
# unigram_tagger  = trainTagger(pos_tagged)
# save tagger
# saveTagger('backend/models/unigram_tagger.pkl', unigram_tagger)
# import tagger
unigram_tagger = importTagger('backend/models/unigram_tagger.pkl')

# print(unigram_tagger.tag(moses.tokenize(sent)))

sent = u"Il faut vraiment clarifier cette affaire et faire connaître ce règlement si particulier qui n'a pas cours ailleurs"
# sent = u""
# sent = u""

tagged_sent = [token[1] for token in unigram_tagger.tag(moses.tokenize(sent ,escape=False))]

print(sent,'\n', tagged_sent ,'\n-----------')

grammar_str = importCFG('backend/models/french_CFG.txt')

grammar = CFG.fromstring(grammar_str.split('\n'))
# print(grammar.productions())

# rd_parser = nltk.RecursiveDescentParser(grammar)

# print(tagged_sent)
# print(grammar)

# print parsing
# parsing kinda working , SLOOWWW :'( THERDET

def parse(sent):
    #Returns nltk.Tree.Tree format output
    a = []  
    parser = nltk.ChartParser(grammar)
    for tree in parser.parse(sent):
        a.append(tree)
    return(a[0]) 

#Gives output as structured tree   
print(parse(tagged_sent))

#Gives tree diagrem in tkinter window
parse(tagged_sent).draw()

# for tree in rd_parser.parse(tagged_sent):
#     t = Tree.fromstring(str(tree))
#     t.draw() 

  
