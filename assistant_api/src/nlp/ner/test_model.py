import spacy


def test_ner_model():
    trained_nlp = spacy.load("models/output/model-best")
    text = "В каких фильмах снимался актер данила козловский. Сколько снял эльдар рязанов. Кто снял фильм зеленая миля. Кто режиссёр фильма титаник. в каких фильмах игра актёр Кузнецов. Какой жанр у фильма ной. Что снял эльдар рязанов."
    doc = trained_nlp(text)

    assert doc.ents[0].text == 'данила козловский'
    assert doc.ents[0].label_ == 'ACTOR'
    assert doc.ents[1].text == 'эльдар рязанов'
    assert doc.ents[1].label_ == 'DIRECTOR'
    assert doc.ents[2].text == 'зеленая миля'
    assert doc.ents[2].label_ == 'MOVIE'
    assert doc.ents[3].text == 'титаник'
    assert doc.ents[3].label_ == 'MOVIE'
    assert doc.ents[4].text == 'Кузнецов'
    assert doc.ents[4].label_ == 'ACTOR'
    assert doc.ents[5].text == 'ной'
    assert doc.ents[5].label_ == 'MOVIE'
    assert doc.ents[6].text == 'эльдар рязанов'
    assert doc.ents[6].label_ == 'DIRECTOR'
