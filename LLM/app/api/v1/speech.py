from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from pyannote.audio import Pipeline
import whisper
import io
import os
import uuid
from services.speech_service import speech_service

router = APIRouter()

HUGGINGFACE_TOKEN = os.getenv("WHISPER_API_KEY")


@router.post("/speech-to-text/")
async def speech_to_text(audio_file: UploadFile = File(...), num_speakers: int = Query(2, ge=1, le=10)):
    try:
        results = await speech_service(audio_file, num_speakers)

        return JSONResponse(content={
            "success": True,
            "segments": results
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
