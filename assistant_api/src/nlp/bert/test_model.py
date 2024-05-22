from bert_classifier import BertClassifier


def test_model():
    classifier = BertClassifier(
        model_path='models/bert.pt',
        tokenizer_path='cointegrated/rubert-tiny',
    )
    assert classifier.predict("Кто автор фильма Тора?") == 0
    assert classifier.predict("Кто снял фильм Тор?") == 0
    assert classifier.predict("Что за жанры у Тора?") == 1
    assert (
        classifier.predict(
            "Позиционные и ключевые аргументы, переданные в функцию должны быть хешируемыми?"
        )
        == 2
    )
