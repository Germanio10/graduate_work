from abc import ABC, abstractmethod
from functools import lru_cache

import spacy
from core.config import CLASSIFICATOR_MODEL_PATH, INTENTS_PATH, NER_MODEL_PATH
from service.classificator.question_classificator import (
    QuestionClassificator,
    get_question_classificator,
)
from spacy.language import Language


class AbstractNLP(ABC):

    @abstractmethod
    def classify_question(self, question: str) -> tuple[str, str] | None:
        pass

    @abstractmethod
    def get_entities(self, text: str) -> tuple[str, str] | None:
        pass


class NLP(AbstractNLP):
    def __init__(self, ner: Language, classificator: QuestionClassificator) -> None:
        self._ner = ner
        self._classificator = classificator

    def classify_question(self, text: str) -> tuple[str, str] | None:
        return self._classificator.classify_question(text)

    def get_entities(self, text: str) -> tuple[str, str] | None:
        doc = self._ner(text)

        if not doc.ents:
            return None
        return doc.ents[0].label_, doc.ents[0].text


@lru_cache
def get_nlp(
    ner: Language = spacy.load(NER_MODEL_PATH),
    classificator: QuestionClassificator = get_question_classificator(
        CLASSIFICATOR_MODEL_PATH,
        INTENTS_PATH,
    ),
) -> AbstractNLP:
    return NLP(ner, classificator)
