from http import HTTPStatus

from fastapi import HTTPException
from speechkit import Session, SpeechSynthesis
from speechkit.exceptions import RequestError


class TextToSpeech:

    def __init__(self, oauth_token, catalog_id):
        self.oauth_token = oauth_token
        self.catalog_id = catalog_id
        self.session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
        self.synthesizeAudio = SpeechSynthesis(self.session)

    def generate_audio_data(self, text, sample_rate=16000):
        try:
            audio_data = self.synthesizeAudio.synthesize_stream(text=text,
                                                                voice='oksana',
                                                                format='lpcm',
                                                                sampleRateHertz=sample_rate)
        except RequestError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Ошибка с подключением к speechkit')
        return audio_data
