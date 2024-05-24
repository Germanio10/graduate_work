import json
from functools import lru_cache

import torch

from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize


class QuestionClassificator:
    def __init__(self) -> None:
        self._init_model()

    def _init_model(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        with open('nlp/classification/train_data/intents.json', 'r') as json_data:
            self.intents = json.load(json_data)

        FILE = "nlp/classification/models/data.pth"
        data = torch.load(FILE)

        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        self.all_words = data['all_words']
        self.tags = data['tags']
        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size, output_size).to(self.device)
        self.model.load_state_dict(model_state)
        self.model.eval()

    def execute(self, question):
        question = tokenize(question)
        X = bag_of_words(question, self.all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(self.device)

        output = self.model(X)
        _, predicted = torch.max(output, dim=1)

        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        print(prob)
        if prob.item() > 0.85:
            for intent in self.intents['intents']:
                if tag == intent["tag"]:
                    return tag
        return None


@lru_cache
def get_question_classificator():
    return QuestionClassificator()
