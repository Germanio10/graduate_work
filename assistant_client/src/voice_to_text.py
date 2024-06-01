from speechkit import Session, ShortAudioRecognition
from speechkit.exceptions import RequestError
from fastapi import HTTPException
from http import HTTPStatus


class VoiceToText:
    def __init__(self, oauth_token, catalog_id):
        self.oauth_token = oauth_token
        self.catalog_id = catalog_id
        self.session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
        self.recognizeShortAudio = ShortAudioRecognition(self.session)

    def voice_recognize(self, audio, sample):
        try:
            text_result = self.recognizeShortAudio.recognize(audio, format='lpcm', sampleRateHertz=sample)
        except RequestError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Ошибка с подлкючением к speechkit")
        return text_result
