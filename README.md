# Speech Recognition API

음성을 텍스트로 변환하는 FastAPI 기반의 REST API 서비스입니다.

## 프로젝트 구조

```
LLM/
├── Dockerfile           # 도커 설정 파일
├── docker-compose.yml   # 도커 컴포즈 설정 파일
└── app/                 # 애플리케이션 코드 (컨테이너의 /app과 동일)
    ├── api/            # API 엔드포인트 구현
    │   └── v1/        # API 버전 1
    ├── core/          # 핵심 설정 및 유틸리티
    └── main.py        # 애플리케이션 진입점
```

## 주요 기능

- 음성 파일(WAV, MP3, OGG)을 텍스트로 변환
- 한국어 음성 인식 지원
- RESTful API 인터페이스
- Swagger UI를 통한 API 문서 제공

## 기술 스택

- FastAPI: 고성능 웹 프레임워크
- Python 3.9
- Docker: 컨테이너화
- SpeechRecognition: 음성 인식 라이브러리
- Google Speech Recognition API: 음성-텍스트 변환 엔진

## API 엔드포인트

### 음성-텍스트 변환 API
- 엔드포인트: `/api/v1/speech/speech-to-text/`
- 메소드: POST
- 입력: 음성 파일 (WAV, MP3, OGG 형식 지원)
- 출력: 변환된 텍스트

## 실행 방법

1. Docker Compose를 사용하여 서비스 시작:
```bash
docker-compose up -d
```

2. API 문서 확인:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 주의사항

- Google Speech Recognition API를 사용하므로 인터넷 연결이 필요합니다.
- 무료 API를 사용하므로 일일 사용량 제한이 있을 수 있습니다.
- 음성 파일의 품질이 좋을수록 인식률이 높아집니다. 