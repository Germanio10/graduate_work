from speechkit import Session, SpeechSynthesis
from speechkit.exceptions import RequestError
from fastapi import HTTPException
from http import HTTPStatus
import pyaudio


class TextRecognizer:

    def __init__(self, oauth_token, catalog_id):
        self.oauth_token = oauth_token
        self.catalog_id = catalog_id
        self.session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
        self.synthesizeAudio = SpeechSynthesis(self.session)

    def play_audio(self, audio_data, num_channels=1,
                   sample_rate=16000, chunk_size=2000) -> None:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=num_channels,
            rate=sample_rate,
            output=True,
            frames_per_buffer=chunk_size
        )

        try:
            for i in range(0, len(audio_data), chunk_size):
                stream.write(audio_data[i:i + chunk_size])
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def generate_audio_data(self, text, sample_rate=16000):
        try:
            audio_data = self.synthesizeAudio.synthesize_stream(text=text,
                                                                voice='oksana',
                                                                format='lpcm',
                                                                sampleRateHertz=sample_rate)
        except RequestError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Ошибка с подключением к speechkit')
        return audio_data
