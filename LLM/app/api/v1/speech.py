from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import speech_recognition as sr
from pydub import AudioSegment
import io
import os

router = APIRouter()

@router.post("/speech-to-text/")
async def speech_to_text(audio_file: UploadFile = File(...)):
    try:
        # 파일 확장자 확인
        file_extension = os.path.splitext(audio_file.filename)[1].lower()
        
        # 파일 내용 읽기
        contents = await audio_file.read()
        audio_bytes = io.BytesIO(contents)
        
        # 음성 인식기 초기화
        recognizer = sr.Recognizer()
        
        # 오디오 파일 처리
        if file_extension in ['.wav', '.mp3', '.ogg']:
            if file_extension != '.wav':
                # mp3/ogg 파일을 wav로 변환
                audio = AudioSegment.from_file(audio_bytes, format=file_extension[1:])
                wav_bytes = io.BytesIO()
                audio.export(wav_bytes, format='wav')
                wav_bytes.seek(0)
                audio_data = sr.AudioFile(wav_bytes)
            else:
                audio_bytes.seek(0)
                audio_data = sr.AudioFile(audio_bytes)
            
            # 음성 인식 수행
            with audio_data as source:
                audio_recorded = recognizer.record(source)
            
            # Google Speech Recognition 사용
            text = recognizer.recognize_google(audio_recorded, language='ko-KR')
            
            return JSONResponse(content={
                "success": True,
                "text": text
            })
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 