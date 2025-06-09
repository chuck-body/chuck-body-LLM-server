# Medical Conversation Speech-to-Text & Tagging API

이 프로젝트는 의료 대화 음성 데이터를 입력받아,
1. 텍스트 변환
2. 화자(의사/환자) 추출 (5회 반복)
3. 대화 요약 및 주요 키워드 기반 태깅
을 한 번에 처리하는 FastAPI 기반 REST API 서비스입니다.

---

## 주요 기능 및 파이프라인

1. **음성 데이터 → 텍스트 변환**
   - Whisper 모델을 사용하여 음성 파일(mp3, wav, ogg, m4a 등)을 텍스트로 변환합니다.
   - PyAnnote를 활용해 2명의 화자(의사/환자)로 분리합니다.

2. **화자 추출 (5회 반복)**
   - 변환된 텍스트에서 화자(SPEAKER_00, SPEAKER_01)를 반복적으로 LLM에 질의하여,  최종적으로 "의사/환자"로 결정합니다.
   - 5회 반복 후에도 미결정 시 임의로 대치합니다.

3. **대화 요약 및 태깅**
   - 화자가 결정된 텍스트를 LLM에 전달하여 대화 내용을 요약합니다.
   - Komoran/Okt 형태소 분석기로 명사 키워드를 미리 추출하여,  LLM이 태그(최대 5개)를 더 잘 추천할 수 있도록 보조합니다.
   - 결과는 summary(요약)와 tags(태그 리스트)로 반환됩니다.

4. **통합 API 제공**
   - 위 1~3 과정을 하나의 API(`/api/v1/audio-to-tags/`)로 제공합니다.
   - 단일 요청으로 음성 → 텍스트 → 화자 추출 → 요약/태깅까지 한 번에 처리합니다.

---

## 프로젝트 구조

```
LLM/
├── Dockerfile
├── requirements.txt
└── app/
    ├── api/v1/
    │   ├── audio_to_tags.py  # 통합 API 엔드포인트
    │   ├── speech.py         # 음성→텍스트
    │   ├── speaker_decision.py # 화자 추출
    │   └── summary.py        # 요약/태깅
    └── services/
        ├── speech_service.py
        ├── speaker_decision_service.py
        ├── summary_service.py
        └── audio_to_tags_service.py
```

---

## API 엔드포인트

### 1. 통합 API: 음성→화자추출→요약/태깅
- **POST** `/api/v1/audio-to-tags/`
- **입력:** `audio_file` (multipart/form-data, mp3/wav/ogg/m4a)
- **출력 예시:**
  ```json
  {
    "summary": "환자가 최근에 겪은 증상에 대해 설명하고, 의사가 진단 및 처방을 안내함.",
    "tags": ["진단", "처방", "증상", "환자", "의사"],
    "origin_text": "의사: ... 환자: ...",
    "success": true
  }
  ```

---

## 실행 방법

1. **도커 빌드 및 실행**
   ```bash
   docker-compose up --build
   ```
2. **API 문서 확인**
   - Swagger UI: http://localhost:8000/docs

---

## 기술 스택

- FastAPI, Python 3.9+
- Whisper, PyAnnote (음성→텍스트, 화자 분리)
- KoNLPy (Okt, Komoran 형태소 분석)
- LLM API (요약/태깅/화자 결정)
- Docker

---

## 참고/주의사항

- LLM, Whisper, PyAnnote 등 외부 API/모델 사용을 위해 환경변수(API KEY 등) 설정 필요
- 오디오 품질이 좋을수록 인식률이 높아집니다
- 대용량 오디오 파일은 처리 시간이 길어질 수 있습니다

---

**문의/기여/이슈는 이 저장소의 Issue 탭을 이용해 주세요!** 