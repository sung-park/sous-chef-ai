import streamlit as st
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 페이지 설정
st.set_page_config(
    page_title="Sous Chef AI",
    page_icon="👨‍🍳",
    layout="wide"
)

# 타이틀
st.title("👨‍🍳 Sous Chef AI")
st.subheader("AI가 만들어주는 맞춤형 레시피")

# Google API Key 로드 확인
api_key = os.getenv("GOOGLE_API_KEY")

st.divider()

# API Key 상태 표시
st.write("### 🔑 API 설정 상태")

if api_key:
    st.success("✅ Google API Key가 성공적으로 로드되었습니다!")
    st.info(f"API Key: {api_key[:10]}...{api_key[-4:]}")
else:
    st.error("❌ Google API Key를 찾을 수 없습니다. .env 파일을 확인해주세요.")
    st.warning("`.env` 파일에 `GOOGLE_API_KEY=your_api_key`를 추가해주세요.")

st.divider()

# 개발 정보
st.write("### 📝 개발 정보")
st.write("""
- **LLM**: Gemini 1.5 Flash (레시피 텍스트 생성)
- **Image**: Imagen 3 (요리 이미지 생성)
- **Framework**: Streamlit (웹 UI)
""")
