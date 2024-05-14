from functools import lru_cache


class VoiceService:
    async def get_data(self, file):

        return {'filename': file.filename}


@lru_cache()
def get_voice_service() -> VoiceService:
    return VoiceService()

