from functools import lru_cache

import spacy


@lru_cache
def get_trained_nlp():
    return spacy.load("nlp/ner/models/output/model-best")
