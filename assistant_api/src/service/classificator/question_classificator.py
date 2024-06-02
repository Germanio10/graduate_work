import json
import random
from functools import lru_cache

import torch
import torch.nn as nn
from core.config import settings
from service.classificator.nltk_utils import bag_of_words, tokenize


class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, hidden_size)
        self.l4 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.LeakyReLU()

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        out = self.relu(out)
        out = self.l4(out)
        return self.l4(out)


class QuestionClassificator:
    def __init__(self, model_file, data_file):
        self.device = torch.device('cpu')
        with open(data_file, 'r') as json_data:
            self.intents = json.load(json_data)
        data = torch.load(model_file)
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        self.all_words = data['all_words']
        self.tags = data['tags']
        model_state = data["model_state"]

        self.model = NeuralNet(input_size, hidden_size, output_size).to(self.device)
        self.model.load_state_dict(model_state)
        self.model.eval()

    def classify_question(self, question) -> tuple[str, str] | None:
        question = tokenize(question)
        X = bag_of_words(question, self.all_words)
        X = torch.tensor(X, dtype=torch.float32).reshape(1, -1).to(self.device)
        output = self.model(X)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]
        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > settings.match_percent:
            for intent in self.intents['intents']:
                if tag == intent['tag']:
                    return tag, random.choice(intent['responses'])

        return None


@lru_cache()
def get_question_classificator(model_file, data_file):
    return QuestionClassificator(model_file, data_file)
