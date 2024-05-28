from deep_translator import GoogleTranslator


class Translator:
    def __init__(self, translator=GoogleTranslator(source='auto', target='en')):
        self.translator = translator

    def translate(self, text_data: str) -> str:
        result = self.translator.translate(text_data)
        return result
