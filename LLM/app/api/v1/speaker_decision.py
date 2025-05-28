from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

import requests
import json

from services.speaker_decision_service import speaker_decision_service

llm_api_key = os.getenv("LLM_API_KEY")

router = APIRouter()


class TextRequest(BaseModel):
    text: str

@router.post("/speaker_decision/")
async def speaker_decision(request: TextRequest):
    try:
        data = speaker_decision_service(request.text)

        return JSONResponse(content={
                            "success": True,
                            "text": data
                            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))