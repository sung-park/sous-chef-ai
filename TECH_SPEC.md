# Sous Chef AI - Technical Specification

## 프로젝트 개요

Sous Chef AI는 사용자가 요리 재료나 요리명을 입력하면, AI가 맞춤형 레시피를 생성하고 완성된 요리 이미지를 제공하는 웹 애플리케이션입니다.

## 목표

- 사용자 친화적인 요리 레시피 생성 경험 제공
- AI 기반 텍스트 및 이미지 생성을 통한 직관적인 요리 가이드 제공
- Google의 최신 AI 기술 스택을 활용한 빠르고 정확한 결과 제공

## 기술 스택

### 1. LLM (Large Language Model)
- **Gemini 1.5 Flash**
  - 용도: 요리 레시피 텍스트 생성
  - 특징: 빠른 응답 속도, 자연스러운 텍스트 생성
  - 활용: 재료 기반 레시피 생성, 조리 방법 상세 설명, 팁 제공

### 2. Image Generation
- **Imagen 3**
  - 용도: 요리 완성샷 이미지 생성
  - 특징: 고품질 이미지 생성, 사실적인 음식 표현
  - 활용: 레시피에 맞는 완성된 요리 이미지 생성

### 3. Web Framework
- **Streamlit**
  - 용도: 웹 UI 프레임워크
  - 특징: 빠른 프로토타이핑, Python 기반, 간단한 배포
  - 활용: 사용자 입력 폼, 결과 출력, 인터랙티브 UI

### 4. 지원 라이브러리
- `google-generativeai`: Google AI API 클라이언트
- `python-dotenv`: 환경 변수 관리
- `watchdog`: 파일 변경 감지

## API 설정

### Google API Key
- `.env` 파일에 `GOOGLE_API_KEY` 설정
- Gemini API와 Imagen API 접근에 사용

## 개발 환경

- **Python**: 3.9+
- **가상환경**: venv
- **패키지 관리**: pip, requirements.txt

## 프로젝트 구조

```
sous-chef-ai/
├── .env                  # API 키 및 환경 변수
├── .gitignore           # Git 제외 파일 목록
├── requirements.txt     # Python 의존성
├── app.py              # 메인 Streamlit 애플리케이션
├── venv/               # Python 가상환경
└── TECH_SPEC.md        # 기술 명세 문서 (본 문서)
```

## 향후 계획

1. 사용자 입력 폼 구현
2. Gemini API를 통한 레시피 생성 기능
3. Imagen API를 통한 이미지 생성 기능
4. UI/UX 개선
5. 레시피 저장 및 공유 기능
