from fastapi import APIRouter
from api.v1.speech import router as speech_router

router = APIRouter()
router.include_router(speech_router, prefix="/speech", tags=["speech"]) 