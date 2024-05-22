import spacy

trained_nlp = spacy.load("models/output/model-best")
text = "Кто снял фильм зеленая миля? Кто режиссёр фильма титаник? "
doc = trained_nlp(text)

for ent in doc.ents:
    print(ent.text, ent.label_)
