import re
import nltk
import math

# path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok.stanford-pos'
path2pos_corpus = 'backend/data/free-french-treebank-master/130612/frwikinews/txt-tok-pos/frwikinews-20130110-pages-articles.txt.tok copy.stanford-pos'

pos_corpus : list  = []
sent_detector = nltk.data.load('tokenizers/punkt/french.pickle')

with open(path2pos_corpus , 'r' , encoding="utf8") as f:
    tokens = []
    for word in re.split(r'\s+|[\n]+', f.read()) :
        if word != '' :
            *token , pos = word.split('_')
            tokens.append(
                ('_'.join(token) , pos)
            )

    sentences = list(sent_detector.sentences_from_tokens(map( lambda x : x[0], tokens)))

    sen_len = 0
    for (idx, val) in enumerate(sentences) :
        pos_corpus.append([(tokens[i][0] , tokens[i][1]) for i in range(sen_len ,sen_len + len(val))])
        sen_len += len(val)
      

        

# for i in range(20) :
#     print('\n------\n',pos_corpus[i])



ngram_tagger = nltk.UnigramTagger(train=pos_corpus , verbose=True) 


text = """À la suite de la parution le matin même d'un article 2=le concernant dans le quotidien Libération, Christophe Hondelatte décide de ne pas présenter le journal de 13 h 00 de France 2.
Il est remplacé au pied levé par Benoît Duquesne.
Dans l'après-midi, la direction de l'information de France 2 annonce que Christophe Hondelatte est relevé de ses fonctions.
Christophe Hondelatte présentait le journal de la mi-journée de France 2 depuis le 6 septembre.
Il avait proposé à plusieurs reprises sa démission à Arlette Chabot.
Le comédien Jacques Villeret est mort à Évreux (Eure) des suites d'une hémorragie interne hépatique.
Il était âgé de 53 ans.
Le président Jacques Chirac a rendu hommage à l'interprète de La Soupe au choux, Papy fait de la Résistance et le Diner de cons en saluant un homme de grande générosité, un merveilleux comédien qui restera comme l'un des grands serviteurs de son art.
Il était l'une des figures familières de la scène et du cinéma français, ralliant toutes les générations autour de personnages attachants et émouvants.
Par sa sincérité, sa simplicité, il savait toucher nos cœurs, dans les rires comme dans les larmes.
C'était un comédien d'un incroyable talent.
Les posters furent installés juste avant le vote.
Des barrières empêchent l'accés pour les voitures; les visiteurs sont filtrés à l'entrée.
Un bus de CRS attend devant le lieu de vote."""

print(ngram_tagger.tag(text.split()))

