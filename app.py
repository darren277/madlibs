""""""
import random
import spacy

nlp = spacy.load("en_core_web_sm")

stopwords = ['it', 'was', 'the', 'of', 'a']


superlatives = [word.lstrip().rstrip() for word in open('data/vocabulary/superlatives.txt', 'r').readlines() if len(word)]
nouns = [word.lstrip().rstrip() for word in open('data/vocabulary/nouns.txt', 'r').readlines() if len(word)]

verbs = [word.lstrip().rstrip() for word in open('data/vocabulary/verbs/verbs.txt', 'r').readlines() if len(word)]
past_participles = [word.lstrip().rstrip() for word in open('data/vocabulary/verbs/past_participle.txt', 'r').readlines() if len(word)]



default_passages = ['taleoftwocities.txt', 'gettysburgaddress.txt', 'tobeornottobe.txt']


PERCENT_OF_WORDS_TO_RANDOMIZE = 0.5



class MadLib:
    def __init__(self, passage: str):
        self.passage = passage

    def generate(self):
        doc = nlp(self.passage)

        s = ""

        for token in doc:
            # print(token.tag_, token)
            if token.pos_ != 'PUNCT' and str(token).lower() not in stopwords:
                if random.random() > PERCENT_OF_WORDS_TO_RANDOMIZE:
                    if token.tag_ == 'JJS':
                        word = random.choice(superlatives)
                        s += " " + word
                    elif token.tag_ == 'NN':
                        word = random.choice(nouns)
                        s += " " + word
                    elif token.tag_ == 'VBN':
                        word = random.choice(past_participles)
                        s += " " + word
                    elif token.tag_ == 'VB':
                        word = random.choice(verbs)
                        s += " " + word
                    else:
                        s += " " + str(token)
                else:
                    s += " " + str(token)
            elif token.pos_ == 'PUNCT':
                s += str(token)
            else:
                s += " " + str(token)
        return s


from flask import Flask, request, make_response, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', default_passage=open('data/passages/'+random.choice(default_passages), 'r').read())

@app.route('/process', methods=['POST'])
def process():
    passage = request.values['passage']

    madlib = MadLib(passage)
    s = madlib.generate()

    return make_response(jsonify({'result': 'success', 'passage': s}), 200)

app.run()
