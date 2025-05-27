from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

import requests
import json

llm_api_key = os.getenv("LLM_API_KEY")

router = APIRouter()


class TextRequest(BaseModel):
    text: str

@router.post("/summary/")
async def summarize_text(request: TextRequest):
    try:
        headers = {
            'Authorization': f"{llm_api_key}",
            'Content-Type': 'application/json'
        }
        data = {
            'model': 'gemma3:12b', 
			'messages': 
				[
        			{'role':'user', 'content': 
					"""
					다음 텍스트 내용을 요약해줘. 최대 300자 이내로 요약해줘.
					"""},
					{'role':'user', 'content': 
					f"""
					{request.text}
					"""}
				]
			}
        response = requests.post('http://hanyang-datascience.duckdns.org:5005/run', headers=headers, json=data)
        print(response.json())
        
        # 여기에 실제 요약 로직을 구현하세요
        # 현재는 간단한 예시로 텍스트의 일부만 반환
        
        return {
            "success": True,
            "summary": response.json()['response']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
