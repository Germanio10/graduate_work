from fastapi import APIRouter, Depends, UploadFile
from services.voice import VoiceService, get_voice_service

router = APIRouter()


@router.post('/uploadfile/',
             description='Получение ответа на голосовой запрос')
async def voice_result(file: UploadFile,
                       voice_service: VoiceService = Depends(get_voice_service)):
    result = await voice_service.get_data(file)
    return result
