from speechkit import Session, SpeechSynthesis
import pyaudio


class TextRecognizer:

    def __init__(self, oauth_token, catalog_id):
        self.oauth_token = oauth_token
        self.catalog_id = catalog_id
        self.session = Session.from_yandex_passport_oauth_token(oauth_token, catalog_id)
        self.synthesizeAudio = SpeechSynthesis(self.session)

    def play_audio(self, audio_data, num_channels=1,
                                    sample_rate=16000, chunk_size=4000) -> None:
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
        audio_data = self.synthesizeAudio.synthesize_stream(text=text,
                                                            voice='oksana',
                                                            format='lpcm',
                                                            sampleRateHertz=sample_rate)
        return audio_data


if __name__ == '__main__':
    oauth_token = "y0_AgAAAABWZr5bAATuwQAAAAEE7C63AADp34-29IdKm4D1jSYn0H0PRqICYQ"
    catalog_id = "b1gekg59n7gjq361p41n"
    text_recognizer = TextRecognizer(oauth_token, catalog_id)

    data = text_recognizer.generate_audio_data('Привет. Сегодня показывают фильм: Железный человек')
    voice = text_recognizer.play_audio(audio_data=data, sample_rate=16000)
