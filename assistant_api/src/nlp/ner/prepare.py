import json
from pathlib import Path

import spacy
from spacy.tokens import DocBin


def read_data(path):
    with open(path) as f:
        text = f.read()
    return json.loads(text)


def prepare_train_data(text, patterns):
    nlp = spacy.load("ru_core_news_md")

    corpus = []

    doc = nlp(text)
    for sent in doc.sents:
        corpus.append(sent.text)

    nlp = spacy.blank("ru")

    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)

    train_data = []
    for sentence in corpus:
        doc = nlp(sentence)
        entities = []

        for ent in doc.ents:
            entities.append([ent.start_char, ent.end_char, ent.label_])
        train_data.append([sentence, {"entities": entities}])
    return train_data


def convert(lang: str, train_data, output_path: Path):
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in train_data:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                print(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)


if __name__ == '__main__':

    full_data = read_data('train.json')

    text_train = full_data['train']['text']
    patterns_train = full_data['train']['patterns']
    text_valid = full_data['valid']['text']
    patterns_valid = full_data['valid']['patterns']
    train_data = prepare_train_data(text_train, patterns_train)
    valid_data = prepare_train_data(text_valid, patterns_valid)

    # for i in train_data:
    #     print(i)

    convert("ru", train_data, "data/train.spacy")
    convert("ru", valid_data, "data/valid.spacy")
