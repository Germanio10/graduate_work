from pathlib import Path

import spacy
from spacy.tokens import DocBin


def prepare_train_data(text, patterns):
    nlp = spacy.load("ru_core_news_sm")

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
    text_train = "Кто сыграл главную роль в фильме волк с Уолл-стрит? Кто является режиссёром фильма интерстеллар? Кто сыграл главную роль в фильме железная леди? Кто снялся в серии фильмов гарри поттер? Кто является режиссёром фильма список шиндлера? Кто сыграл главную роль в фильме белла и бестия? Кто является режиссёром фильма убить билла? Кто снялся в фильме железный человек? Кто рейтинг у фильма железный человек?"
    patterns_train = [
        {"label": "MOVIE", "pattern": "волк с уолл-стрит"},
        {"label": "MOVIE", "pattern": "интерстеллар"},
        {"label": "MOVIE", "pattern": "железная леди"},
        {"label": "MOVIE", "pattern": "гарри поттер"},
        {"label": "MOVIE", "pattern": "список Шиндлера"},
        {"label": "MOVIE", "pattern": "убить билла"},
        {"label": "MOVIE", "pattern": "железный человек"},
    ]

    valid_train = "Что за актер был в фильме армагедон? Кто рейтинг у фильма крестный отец? Кто сыграл главную роль в фильме армагедон? Кто снялся в серии фильмов терминатор? Кто является режиссёром фильма исчезнувшая? Кто сыграл главную роль в фильме крестный отец? Кто является режиссёром фильма красотка? Кто снялся в фильме красотка?"
    patterns_valid = [
        {"label": "MOVIE", "pattern": "армагедон"},
        {"label": "MOVIE", "pattern": "крестный отец"},
        {"label": "MOVIE", "pattern": "терминатор"},
        {"label": "MOVIE", "pattern": "красотка"},
    ]

    train_data = prepare_train_data(text_train, patterns_train)
    valid_data = prepare_train_data(text_train, patterns_train)

    convert("ru", train_data, "data/train.spacy")
    convert("ru", valid_data, "data/valid.spacy")
