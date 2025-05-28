from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

import requests
import json

from services.summary_service import summary_service

llm_api_key = os.getenv("LLM_API_KEY")

router = APIRouter()


class TextRequest(BaseModel):
    text: str


@router.post("/summary/")
async def summarize_text(request: TextRequest):
    try:
        data = summary_service(request.text)
        
        # 키 추가
        data['success'] = True
        
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))