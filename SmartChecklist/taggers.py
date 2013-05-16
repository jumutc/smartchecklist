import nltk
import os.path
import cPickle as pickle
from nltk.corpus import brown
from nltk.tag.brill import *
from settings import HUNPOS_TAGGER_MODEL_PATH, DEFAULT_TAGGER_MODEL_PATH

def get_hunpos_tagger():
    path = os.path.expanduser(HUNPOS_TAGGER_MODEL_PATH)
    return nltk.tag.HunposTagger(path)

def get_default_tagger(reload_model):
    path = os.path.expanduser(DEFAULT_TAGGER_MODEL_PATH)
    if reload_model or not os.path.exists(path):
        #Regexp tagger
        regexp_tagger = nltk.RegexpTagger(
                [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
                    (r'(The|the|A|a|An|an)$', 'AT'),   # articles
                    (r'.*able$', 'JJ'),                # adjectives
                    (r'.*ness$', 'NN'),                # nouns formed from adjectives
                    (r'.*ly$', 'RB'),                  # adverbs
                    (r'.*s$', 'NNS'),                  # plural nouns
                    (r'.*ing$', 'NN'),                 # transitive nouns
                    (r'.*ings$', 'NNS'),               # transitive plural nouns
                    (r'.*ed$', 'VBD'),                 # past tense verbs
                    (r'.*', 'NN')                      # nouns (default)
                ])

        #Unigram tagger
        brown_train = brown.tagged_sents()
        default = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)

        #Brill tagger
        templates = [
            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,1)),
            SymmetricProximateTokensTemplate(ProximateTagsRule, (2,2)),
            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,2)),
            SymmetricProximateTokensTemplate(ProximateTagsRule, (1,3)),
            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,1)),
            SymmetricProximateTokensTemplate(ProximateWordsRule, (2,2)),
            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,2)),
            SymmetricProximateTokensTemplate(ProximateWordsRule, (1,3)),
            ProximateTokensTemplate(ProximateTagsRule, (-1, -1), (1,1)),
            ProximateTokensTemplate(ProximateWordsRule, (-1, -1), (1,1)),
            ]
        trainer = FastBrillTaggerTrainer(initial_tagger=default, templates=templates, trace=3, deterministic=True)
        tagger = trainer.train(brown_train, max_rules=50)
        pickle.dump(tagger, open(path, 'w'))
        return tagger
    else:
        return pickle.load(open(path, 'r'))
