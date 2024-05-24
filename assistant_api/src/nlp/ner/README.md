# Создание модели для распознавание именованных объектов (актеры, фильмы, режиссеры)

Подготовка данных:
```shell
python3 prepare.py
```
Обучение модели:
```shell
python3 -m spacy train data/config.cfg --output ./models/output
```
Тестирование модели:
```shell
python3 test_model.py
```