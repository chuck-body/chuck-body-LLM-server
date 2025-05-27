from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 이 줄 추가
from api.v1 import speech, summary

app = FastAPI(title="LLM Server")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(speech.router, prefix="/api/v1", tags=["speech"])
app.include_router(summary.router, prefix="/api/v1", tags=["summary"])

@app.get("/")
async def root():
    return {"message": "LLM Server is running"}