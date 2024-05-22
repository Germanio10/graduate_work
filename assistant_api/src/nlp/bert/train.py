import pandas as pd
from bert_classifier import BertTrainClassifier

if __name__ == '__main__':
    train_data = pd.read_csv('train_data/train.csv')
    valid_data = pd.read_csv('train_data/valid.csv')

    classifier = BertTrainClassifier(
        model_path='cointegrated/rubert-tiny',
        tokenizer_path='cointegrated/rubert-tiny',
        n_classes=3,
        epochs=2,
        model_save_path='bert.pt',
    )

    classifier.preparation(
        X_train=list(train_data['text']),
        y_train=list(train_data['label']),
        X_valid=list(valid_data['text']),
        y_valid=list(valid_data['label']),
    )

    classifier.train()

# texts = list(test_data['text'])
# labels = list(test_data['label'])

# # predictions = [classifier.predict(t) for t in texts]

# print(classifier.predict("Кто автор фильма Тора?", 'bert.pt'))


# precision, recall, f1score = precision_recall_fscore_support(labels, predictions, average='macro')[
#     :3
# ]

# print(f'precision: {precision}, recall: {recall}, f1score: {f1score}')
