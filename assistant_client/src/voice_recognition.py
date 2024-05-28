import io
import wave
import pyaudio
from speechkit import Session, ShortAudioRecognition
from speechkit.exceptions import RequestError
from fastapi import HTTPException
from http import HTTPStatus


class VoiceRecognizer:

    def __init__(self, oauth_token, catalog_id):
        self.oauth_token = oauth_token
        self.catalog_id = catalog_id
        self.session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
        self.recognizeShortAudio = ShortAudioRecognition(self.session)

    def record_audio(self, seconds, sample_rate,
                     chunk_size=4000, num_channels=1) -> bytes:

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=num_channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=chunk_size
        )
        frames = []
        try:
            for i in range(0, int(sample_rate / chunk_size * seconds)):
                data = stream.read(chunk_size)
                frames.append(data)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

        container = io.BytesIO()
        wf = wave.open(container, 'wb')
        wf.setnchannels(num_channels)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))
        container.seek(0)
        return container

    def audio_to_text(self, audio, sample):
        try:
            text_result = self.recognizeShortAudio.recognize(audio, format='lpcm', sampleRateHertz=sample)
        except RequestError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Ошибка с подлкючением к speechkit")
        return text_result
