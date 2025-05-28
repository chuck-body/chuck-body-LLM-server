from fastapi import APIRouter, UploadFile, File, HTTPException
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


@router.post("/audio-to-tags/")
async def audio_to_tags(audio_file: UploadFile = File(...)):
    try:
        results = await audio_to_tags_service(audio_file)
        
        
        results['success'] = True
        
        return JSONResponse(content=results)
        return JSONResponse(content={
            "success": True,
            "segments": results
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
