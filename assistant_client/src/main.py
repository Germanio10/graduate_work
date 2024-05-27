import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from text_recognition import TextRecognizer
from voice_recognition import VoiceRecognizer

TOKEN = "y0_AgAAAABWZr5bAATuwQAAAAEE7C63AADp34-29IdKm4D1jSYn0H0PRqICYQ"
CATALOG = "b1gekg59n7gjq361p41n"
SAMPLE_RATE = 16000


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Голосовой ассистент")

        self.layout = QVBoxLayout()

        self.button = QPushButton("Задайте вопрос")
        self.button.clicked.connect(self.process_voice)
        self.layout.addWidget(self.button)

        self.request_label = QLabel("Вопрос: ")
        self.layout.addWidget(self.request_label)

        self.response_label = QLabel("Ответ: ")
        self.layout.addWidget(self.response_label)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

    def process_voice(self):
        # Clear the labels before starting the voice recognition process
        self.request_label.setText("Request: ")
        self.response_label.setText("Response: ")

        voice_recognizer = VoiceRecognizer(TOKEN, CATALOG)
        text_recognizer = TextRecognizer(TOKEN, CATALOG)

        voice_data = voice_recognizer.record_audio(3, SAMPLE_RATE)
        text = voice_recognizer.audio_to_text(voice_data, SAMPLE_RATE)
        self.request_label.setText(f"Request: {text}")

        response = requests.post(
            'http://127.0.0.1:8000/api/v1/assistant/',
            json={'text': text}
        )
        search_service_answer = response.json().get('answer')
        self.response_label.setText(f"Response: {search_service_answer}")

        data_for_voice = text_recognizer.generate_audio_data(search_service_answer)
        text_recognizer.play_audio(audio_data=data_for_voice)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
