import os
import io
from fastapi import HTTPException
from pydub import AudioSegment
import uuid
import whisper
from pyannote.audio import Pipeline

HUGGINGFACE_TOKEN = os.getenv("WHISPER_API_KEY")

async def speech_service(audio_file, num_speakers: int = 2):
    print("speech_service start")
    file_extension = os.path.splitext(audio_file.filename)[1].lower()
    print(f"file_extension: {file_extension}")
    if file_extension not in ['.mp3', '.wav', '.ogg', '.m4a']:
        raise HTTPException(status_code=400, detail="지원하지 않는 파일 형식입니다.")

    # 파일 읽기
    contents = await audio_file.read()
    audio_bytes = io.BytesIO(contents)

    # 파일을 WAV로 변환 (in-memory)
    if file_extension != '.wav':
        audio = AudioSegment.from_file(audio_bytes, format=file_extension[1:])
        wav_bytes = io.BytesIO()
        audio.export(wav_bytes, format='wav')
        wav_bytes.seek(0)
    else:
        wav_bytes = audio_bytes
        wav_bytes.seek(0)

    # 임시 WAV 파일 저장
    temp_filename = f"{uuid.uuid4()}.wav"
    with open(temp_filename, "wb") as f:
        f.write(wav_bytes.read())

    # Whisper 모델 로드 및 자막 추출
    whisper_model = whisper.load_model("base") #base 모델. tiny -> base -> small -> medium -> large 순서로 정확도 향상
    whisper_result = whisper_model.transcribe(temp_filename, word_timestamps=True)
    segments = whisper_result["segments"]

    # PyAnnote 화자 분리
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=HUGGINGFACE_TOKEN)
    diarization = pipeline(temp_filename, num_speakers = num_speakers) #화자의 수를 2명으로 제한

    # 가장 많이 겹치는 화자 하나만 매칭
    def get_best_speaker(segment, diarization):
        max_overlap = 0
        best_speaker = None
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            overlap_start = max(segment["start"], turn.start)
            overlap_end = min(segment["end"], turn.end)
            duration = max(0, overlap_end - overlap_start)
            if duration > max_overlap:
                max_overlap = duration
                best_speaker = speaker
        return best_speaker

    results = []
    for segment in segments:
        speaker = get_best_speaker(segment, diarization)
        results.append({
            "speaker": speaker,
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"]
        })

    os.remove(temp_filename)
    print("speech_service done")
    return results