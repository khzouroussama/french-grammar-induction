import re
import nltk
import math
from sacremoses import MosesTokenizer
from pickle import dump ,load
from operator import itemgetter
from os import system, name 

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


def SaveTrainedTagger(outputFile,tagger) :
    output = open(outputFile, 'wb')
    dump(tagger, output, -1)
    output.close()

def loadTrainedTagger(inputfile) :
    input = open(inputfile, 'rb')
    tagger = load(input)
    input.close()
    return tagger



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
path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok.stanford-pos'
# path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok copy.stanford-pos'

sent_detector = nltk.data.load('tokenizers/punkt/french.pickle') 

# TRAIN 
################################
# posTaggedCorpus = loadCorpus(path2pos_corpus, sent_tokenizer=sent_detector.sentences_from_tokens ) 
# size = int(len(posTaggedCorpus) * 0.9)
# train_sents = posTaggedCorpus[:size]
# test_sents = posTaggedCorpus[size:]
# unigram_tagger = nltk.UnigramTagger(train=posTaggedCorpus , verbose=True)
# print('(train={} , test={} , evaluate={})'.format(size ,len(posTaggedCorpus) ,unigram_tagger.evaluate(test_sents)))
# SaveTrainedTagger('backend/models/unigram_tagger.pkl', unigram_tagger)
# LOAD 
################################
# unigram_tagger = loadTrainedTagger('backend/models/unigram_tagger.pkl')


# moses = MosesTokenizer(lang='fr')
# print(getPOSSentencesFromText(text, unigram_tagger,sent_detector.sentences_from_tokens, moses.tokenize))



##########################################
#  IMPLEMENTING SELAB_GUESSOUM THE ALGORITHM
##########################################
pos_tagged = loadCorpus(path2pos_corpus)

def NGramExtraction(pos_tagged) : 
    ngrams = []
    for sent in pos_tagged :
        for i in range(len(sent)) :
            ngrams.extend(nltk.ngrams(map(lambda x : x[1] ,sent),i+1))
    return ngrams

def getMaxFromFreqDist(freq):
    for elm in sorted(freq.items(), key=itemgetter(1), reverse=True) :
        # print(elm)
        if len(elm[0]) == 1 :
            if not elm[0][0].startswith('#R') :
                return elm[0]
        else :
            return elm[0]
    # return freq.max()

def Substitution(pos_tagged , R , non_terminal ) :
    result = []
    for sen in pos_tagged : 
        new_sen = sen
        for i in range(len(sen) - len(R)+1) :
            if list(map(lambda x:x[1],sen[i:i + len(R)])) == list(R) :
                new_sen = new_sen[:i]+[(non_terminal,non_terminal)]+new_sen[i + len(R):]
        result.append(new_sen)

    return result

# print(tuple(word[1] for word in pos_tagged[0] ) )
# print(  pos_tagged[0])
# print(len(pos_tagged))

# freq = nltk.FreqDist(NGramExtraction(pos_tagged))

# print(sorted(freq.items(), key=itemgetter(1), reverse=True)[:40])

loop_max = 50
R = []
# START ALGORITHM 
for i in range(loop_max) : #FIXME 
    system('clear')
    print('Building Grammar : \n[{}] {}%'.format('='*(i+1)+' '*(loop_max-i-1) , int(((i+1) / loop_max)*100)) )
    freq = nltk.FreqDist(NGramExtraction(pos_tagged))
    maxFreq = getMaxFromFreqDist(freq)
    R.append(maxFreq)
    # print(maxFreq)
    pos_tagged = Substitution(pos_tagged, maxFreq, '#R'+str(i))




# print(pos_tagged[0])
print('Grammar : \n')
for (idx ,val) in enumerate(R) :
    print('R'+str(idx) ,'->' ,' '.join( val))
