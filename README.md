# 🍳 Sous Chef AI

AI가 만들어주는 맞춤형 레시피 & 요리 사진

Google의 최신 AI 기술(Gemini 2.5 Flash, Imagen 4.0)을 활용하여 요리 레시피를 자동으로 생성하고, 각 조리 단계별 사진까지 함께 제공하는 웹 서비스입니다.

## ✨ 주요 기능

- **AI 레시피 생성**: Gemini 2.5 Flash를 활용한 감성적이고 친절한 말투의 레시피 생성
- **단계별 이미지 생성**: Imagen 4.0으로 각 조리 과정을 시각화한 사진 자동 생성
- **실시간 진행 상황**: 이미지 생성 과정을 실시간으로 확인 가능
- **블로그 포스팅 지원**: 생성된 레시피를 마크다운 형식으로 다운로드
- **스마트 조리 도구 인식**: 조리 단계에 맞는 적절한 도구(냄비, 후라이팬, 도마 등)로 이미지 생성

## 🛠️ 기술 스택

- **LLM**: Google Gemini 2.5 Flash
- **Image Generation**: Google Imagen 4.0
- **Web Framework**: Streamlit
- **Language**: Python 3.x

## 📦 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/sung-park/sous-chef-ai.git
cd sous-chef-ai
```

2. 가상환경 생성 및 활성화
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 패키지 설치
```bash
pip install -r requirements.txt
```

4. 환경 변수 설정
`.env` 파일을 생성하고 Google API Key를 설정합니다:
```
GOOGLE_API_KEY=your_api_key_here
```

## 🚀 사용 방법

1. Streamlit 앱 실행
```bash
streamlit run app.py
```

2. 브라우저에서 `http://localhost:8501` 접속

3. 요리 이름 입력 (예: 김치찌개, 된장찌개, 파스타 등)

4. "레시피 & 사진 생성하기" 버튼 클릭

5. 생성된 레시피와 단계별 사진 확인

6. 사이드바에서 블로그 포스팅용 텍스트 다운로드 가능

## 🧪 테스트

레시피 생성 기능을 테스트하려면:
```bash
python test_brain.py
```

## 📁 프로젝트 구조

```
sous-chef-ai/
├── app.py              # Streamlit 웹 애플리케이션
├── chef_brain.py       # RecipeAgent 핵심 로직
├── test_brain.py       # 테스트 스크립트
├── list_models.py      # 사용 가능한 모델 확인
├── requirements.txt    # 의존성 패키지
├── .env               # 환경 변수 (API Key)
├── .gitignore         # Git 제외 파일
└── temp/              # 생성된 이미지 저장 폴더
```

## 🔑 API Key 발급

Google AI Studio에서 API Key를 발급받으세요:
- [Google AI Studio](https://aistudio.google.com/app/apikey)

## 📝 라이선스

MIT License

## 🤝 기여

이슈 및 풀 리퀘스트는 언제나 환영합니다!

---

Made with ❤️ using Google Gemini & Imagen
