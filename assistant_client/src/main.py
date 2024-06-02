import sys
from http import HTTPStatus

import requests
from audio_player import AudioPlayer
from core.config import settings
from fastapi import HTTPException
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QApplication, QFrame, QLabel, QMainWindow,
                             QPushButton, QVBoxLayout, QWidget)
from recorder import Recorder
from speechkit.exceptions import RequestError
from text_to_speech import TextToSpeech
from voice_to_text import VoiceToText

SAMPLE_RATE = 16000


class VoiceAssistant:
    def __init__(self):
        self.voice_to_text = VoiceToText(settings.yandex_settings.token, settings.yandex_settings.catalog)
        self.text_to_speech = TextToSpeech(settings.yandex_settings.token, settings.yandex_settings.catalog)
        self.recorder = Recorder()
        self.audio_player = AudioPlayer()

    def process_voice(self, main_window):
        main_window.request_label.setText("Вопрос: ")
        main_window.response_label.setText("Ответ: ")

        voice_data = self.recorder.record_audio(3, SAMPLE_RATE)
        try:
            text = self.voice_to_text.voice_recognize(voice_data, SAMPLE_RATE)
        except RequestError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Ошибка с подключением к speechkit')
        main_window.request_label.setText(f"Вопрос: {text}")

        response = requests.post(
            settings.yandex_settings.project_url,
            json={'text': text}
        )
        search_service_answer = response.json().get('answer')
        main_window.response_label.setText(f"Ответ: {search_service_answer}")

        try:
            data_for_voice = self.text_to_speech.generate_audio_data(search_service_answer)
        except RequestError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Ошибка с подключением к speechkit')
        self.audio_player.play_audio(audio_data=data_for_voice)


class MainWindow(QMainWindow):
    def __init__(self, assistant: VoiceAssistant):
        super().__init__()

        self.setWindowTitle("Голосовой ассистент")
        self.setGeometry(300, 300, 400, 300)

        font = QFont("Arial", 12)

        main_layout = QVBoxLayout()

        self.button = QPushButton("Задайте вопрос")
        self.button.setFont(font)
        self.button.clicked.connect(lambda: assistant.process_voice(self))
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


def main():
    app = QApplication(sys.argv)

    assistant = VoiceAssistant()
    window = MainWindow(assistant)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
