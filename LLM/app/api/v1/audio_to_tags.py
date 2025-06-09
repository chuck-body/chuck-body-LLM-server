from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from pydub import AudioSegment
from pyannote.audio import Pipeline
import whisper
import io
import os
import uuid

from services.audio_to_tags_service import audio_to_tags_service

router = APIRouter()

HUGGINGFACE_TOKEN = os.getenv("WHISPER_API_KEY")


@router.post("/audio-to-tags")
async def audio_to_tags(
    audio_file: UploadFile = File(...),
    num_speakers: int = Query(..., ge=1, le=10)  # Form으로 변경, 유효성 검사는 그대로
):
    try:
        results = await audio_to_tags_service(audio_file, num_speakers=num_speakers)
        
        
        results['success'] = True
        
        return JSONResponse(content=results)
        return JSONResponse(content={
            "success": True,
            "segments": results
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
