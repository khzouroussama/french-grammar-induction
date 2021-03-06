import os
import logging
from PIL import Image
import io
import base64
from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import nltk
from sacremoses import MosesTokenizer
from backend.algo import parse,importCFG,importTagger, FormatGrammarAsCFG, InductGrammar, loadCorpusFromStr

tagger = importTagger('backend/models/unigram_tagger.pkl')



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



from pyvirtualdisplay import Display
display = Display(visible=0, size=(1400, 900))
display.start()

# This code creates a virtual display to draw game images on. 
# If you are running locally, just ignore it
import os
if type(os.environ.get("DISPLAY")) is not str or len(os.environ.get("DISPLAY"))==0:
    os.system('bash xvfb start')
    os.system('export DISPLAY :1')

@app.get("/")
def read_root():
    return {"rules": "nothing here"}


@app.get("/analyze")
def analyze_text( sent: Optional[str] = None):
    grammar_str = importCFG('backend/models/french_CFG.txt')
    moses = MosesTokenizer(lang='fr')
    grammar = nltk.CFG.fromstring(grammar_str.split('\n'))

    tagged_sent = tagger.tag(moses.tokenize(sent ,escape=False))
    tags = [token[1] for token in tagged_sent]

    parsed = []
    image = ''
    try :
        parsed = parse(tags, grammar)
        from nltk.draw.tree import TreeView
        (x0, y0, w, h) = TreeView(parsed)._cframe.scrollregion()
        ps = TreeView(parsed)._cframe._canvas.postscript(
            x=x0,
            y=y0,
            width=w + 2,
            height=h + 2,
            pagewidth=w + 2,  # points = 1/72 inch
            pageheight=h + 2,  # points = 1/72 inch
            pagex=0,
            pagey=0,
            colormode='color'
        )
        ps = ps.replace(" 0 scalefont ", " 9 scalefont ")
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.load(scale=5)
        image_out = io.BytesIO()
        img.save(image_out, format="png")
        # image_out.seek(0)
        image = base64.b64encode(image_out.getvalue()).decode()
    except Exception as e: 
        logging.exception("An exception was thrown!")

    return {"sentence": sent, "tagged" : tagged_sent, "parsed": str(parsed) , "image":image}





@app.get("/generate")
def generate( corpus: Optional[str] = None , test: Optional[str] = None):
    moses = MosesTokenizer(lang='fr')

    pos_tagged = loadCorpusFromStr(corpus)
    grammar_str = FormatGrammarAsCFG(InductGrammar(pos_tagged))



    grammar = nltk.CFG.fromstring(grammar_str.split('\n'))

    parsed = []
    valid = []
    not_valide = []

    for s in test.split('$') : 
        try :
            tagged_sent = [token[1] for token in tagger.tag(moses.tokenize(s ,escape=False))]
            parsed = parse(tagged_sent,grammar)
            if parsed != None : 
                valid.append((s,str(parsed)))
            else: 
                not_valide.append(s)
        except :
            not_valide.append(s)

    return {"grammar" : grammar_str , "test_results" : { "valide" : valid,"not_valide" : not_valide } }
