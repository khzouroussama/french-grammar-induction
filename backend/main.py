from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import nltk
from sacremoses import MosesTokenizer
from algo import parse,importCFG,importTagger

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"rules": "nothing here"}


@app.get("/analyze")
def read_item( sent: Optional[str] = None):
    grammar_str = importCFG('models/french_CFG.txt')
    tagger = importTagger('models/unigram_tagger.pkl')
    moses = MosesTokenizer(lang='fr')
    grammar = nltk.CFG.fromstring(grammar_str.split('\n'))

    tagged_sent = tagger.tag(moses.tokenize(sent ,escape=False))
    tags = [token[1] for token in tagged_sent]

    parsed = []
    try :
        parsed = parse(tags, grammar)
    except:
        print("Something else went wrong")

    return {"sentence": sent, "tagged" : tagged_sent, "parsed": str(parsed)}
