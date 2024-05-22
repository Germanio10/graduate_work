import requests
from text_recognition import TextRecognizer
from translator import Translator
from voice_recognition import VoiceRecognizer

TOKEN = ""
CATALOG = ""
SAMPLE_RATE = 16000


def main():
    voice_recognizer = VoiceRecognizer(TOKEN, CATALOG)
    text_recognizer = TextRecognizer(TOKEN, CATALOG)
    translator = Translator()

    voice_data = voice_recognizer.record_audio(3, SAMPLE_RATE)
    text = voice_recognizer.audio_to_text(voice_data, SAMPLE_RATE)
    translated_text = translator.translate(text).lower()
    response = requests.post(
        'http://127.0.0.1:8000/api/v1/assistant/', json={'text': translated_text}
    )
    search_service_answer = response.json().get('answer')
    data_for_voice = text_recognizer.generate_audio_data(search_service_answer)
    voice = text_recognizer.play_audio(audio_data=data_for_voice)


if __name__ == '__main__':
    main()
