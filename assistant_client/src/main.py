import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QFrame
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from text_recognition import TextRecognizer
from voice_recognition import VoiceRecognizer
from core.config import settings

SAMPLE_RATE = 16000


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Голосовой ассистент")
        self.setGeometry(300, 300, 400, 300)

        font = QFont("Arial", 12)

        main_layout = QVBoxLayout()

        self.button = QPushButton("Задайте вопрос")
        self.button.setFont(font)
        self.button.clicked.connect(self.process_voice)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        main_layout.addWidget(self.button, alignment=Qt.AlignCenter)

        self.request_label = QLabel("Вопрос: ")
        self.request_label.setFont(font)
        self.request_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.request_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.request_label.setStyleSheet("padding: 10px; background-color: #f0f0f0;")
        main_layout.addWidget(self.request_label)

        self.response_label = QLabel("Ответ: ")
        self.response_label.setFont(font)
        self.response_label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.response_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.response_label.setStyleSheet("padding: 10px; background-color: #f0f0f0;")
        main_layout.addWidget(self.response_label)

        container = QWidget()
        container.setLayout(main_layout)

        self.setCentralWidget(container)

    def process_voice(self):
        self.request_label.setText("Вопрос: ")
        self.response_label.setText("Ответ: ")

        voice_recognizer = VoiceRecognizer(settings.yandex_settings.token, settings.yandex_settings.catalog)
        text_recognizer = TextRecognizer(settings.yandex_settings.token, settings.yandex_settings.catalog)

        voice_data = voice_recognizer.record_audio(3, SAMPLE_RATE)
        text = voice_recognizer.audio_to_text(voice_data, SAMPLE_RATE)
        self.request_label.setText(f"Вопрос: {text}")

        response = requests.post(
            'http://127.0.0.1:8000/api/v1/assistant/',
            json={'text': text}
        )
        search_service_answer = response.json().get('answer')
        self.response_label.setText(f"Ответ: {search_service_answer}")

        data_for_voice = text_recognizer.generate_audio_data(search_service_answer)
        text_recognizer.play_audio(audio_data=data_for_voice)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
