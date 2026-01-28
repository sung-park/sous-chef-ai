import streamlit as st
import os
from pathlib import Path
from chef_brain import RecipeAgent

# 페이지 설정
st.set_page_config(
    page_title="Sous Chef AI",
    page_icon="🍳",
    layout="wide"
)

# Session State 초기화
if 'recipe' not in st.session_state:
    st.session_state.recipe = None
if 'step_images' not in st.session_state:
    st.session_state.step_images = []
if 'dish_name' not in st.session_state:
    st.session_state.dish_name = ""

# 타이틀
st.title("🍳 Sous Chef AI")
st.subheader("AI가 만들어주는 맞춤형 레시피 & 요리 사진")

st.divider()

# 메인 컨텐츠
col1, col2 = st.columns([2, 1])

with col1:
    st.write("### 🥘 어떤 요리를 만들고 싶으세요?")

    # 입력 폼
    dish_name = st.text_input(
        "요리 이름을 입력하세요",
        placeholder="예: 김치찌개, 된장찌개, 파스타, 돈까스...",
        key="dish_input"
    )

    # 생성 버튼
    generate_button = st.button(
        "🎨 레시피 & 사진 생성하기",
        type="primary",
        use_container_width=True
    )

    st.divider()

    # 버튼 클릭 시 레시피 및 이미지 생성
    if generate_button and dish_name:
        st.session_state.dish_name = dish_name

        try:
            # RecipeAgent 초기화
            agent = RecipeAgent()

            # 1단계: 레시피 텍스트 생성
            with st.spinner(f"🤖 Gemini 2.5가 '{dish_name}' 레시피를 고민 중입니다..."):
                recipe = agent.generate_recipe(dish_name)
                st.session_state.recipe = recipe

            st.success("✅ 레시피 생성 완료!")

            # 2단계: 단계별 이미지 생성
            with st.spinner(f"📸 Imagen 4.0이 '{dish_name}' 조리 단계별 사진을 촬영 중입니다... (총 {len(recipe['steps'])}장)"):
                step_images = agent.generate_step_images(dish_name, recipe)
                st.session_state.step_images = step_images

            success_count = len([img for img in step_images if img])
            st.success(f"✅ 조리 단계별 사진 생성 완료! ({success_count}/{len(recipe['steps'])}장)")

        except Exception as e:
            st.error(f"❌ 오류가 발생했습니다: {e}")
            st.session_state.recipe = None
            st.session_state.step_images = []

    elif generate_button and not dish_name:
        st.warning("⚠️ 요리 이름을 입력해주세요!")

with col2:
    st.write("### ℹ️ 사용 방법")
    st.info("""
    1. 왼쪽에 요리 이름 입력
    2. 버튼을 클릭하여 생성
    3. AI가 레시피와 사진을 만들어드립니다!

    **기술 스택:**
    - 🤖 Gemini 2.5 Flash
    - 🎨 Imagen 4.0
    - 🚀 Streamlit
    """)

st.divider()

# 레시피 결과 표시
if st.session_state.recipe:
    recipe = st.session_state.recipe

    # 레시피 제목
    st.markdown(f"## 📌 {recipe['title']}")
    st.markdown(f"**⏱️ 소요 시간:** {recipe['cooking_time']}")

    st.divider()

    # 재료
    st.markdown("### 🥘 재료")
    ingredients_col1, ingredients_col2 = st.columns(2)
    mid_point = len(recipe['ingredients']) // 2

    with ingredients_col1:
        for i, ingredient in enumerate(recipe['ingredients'][:mid_point], 1):
            st.write(f"{i}. {ingredient}")

    with ingredients_col2:
        for i, ingredient in enumerate(recipe['ingredients'][mid_point:], mid_point + 1):
            st.write(f"{i}. {ingredient}")

    st.divider()

    # 조리 과정 (단계별 이미지 포함)
    st.markdown("### 👨‍🍳 조리 과정")

    for i, step in enumerate(recipe['steps'], 1):
        with st.expander(f"**{i}단계**", expanded=True):
            # 2단 레이아웃: 왼쪽은 설명, 오른쪽은 이미지
            step_col1, step_col2 = st.columns([3, 2])

            with step_col1:
                st.write(step)

            with step_col2:
                # 단계별 이미지 표시
                if st.session_state.step_images and i <= len(st.session_state.step_images):
                    image_path = st.session_state.step_images[i - 1]
                    if image_path and Path(image_path).exists():
                        st.image(
                            image_path,
                            caption=f"{i}단계",
                            use_container_width=True
                        )
                    else:
                        st.info(f"{i}단계 이미지를 생성하지 못했습니다.")
                else:
                    st.info("이미지 생성 중...")

# 사이드바 - 블로그 포스팅용 텍스트
if st.session_state.recipe:
    with st.sidebar:
        st.markdown("## 📝 블로그 포스팅용")
        st.write("아래 텍스트를 복사해서 사용하세요!")

        # 블로그 포스팅용 텍스트 생성
        blog_text = f"""# {st.session_state.recipe['title']}

⏱️ **소요 시간:** {st.session_state.recipe['cooking_time']}

## 🥘 재료

"""

        for i, ingredient in enumerate(st.session_state.recipe['ingredients'], 1):
            blog_text += f"{i}. {ingredient}\n"

        blog_text += "\n## 👨‍🍳 조리 과정\n\n"

        for i, step in enumerate(st.session_state.recipe['steps'], 1):
            blog_text += f"### {i}단계\n\n{step}\n\n"

        blog_text += "\n---\n\n🤖 AI로 생성된 레시피입니다. (Sous Chef AI)\n"

        # 텍스트 박스로 표시 (복사 가능)
        st.text_area(
            "레시피 전문",
            blog_text,
            height=400,
            help="Ctrl+A로 전체 선택 후 Ctrl+C로 복사하세요"
        )

        st.download_button(
            label="📥 텍스트 파일로 다운로드",
            data=blog_text,
            file_name=f"{st.session_state.dish_name}_recipe.md",
            mime="text/markdown"
        )

# 하단 정보
st.divider()
with st.expander("🔧 개발 정보"):
    st.write("""
    **Sous Chef AI**는 Google의 최신 AI 기술을 활용한 레시피 생성 서비스입니다.

    - **LLM**: Gemini 2.5 Flash (텍스트 생성)
    - **Image**: Imagen 4.0 (이미지 생성)
    - **Framework**: Streamlit (웹 UI)
    - **GitHub**: [sous-chef-ai](https://github.com/yourusername/sous-chef-ai)

    Made with ❤️ by Sous Chef AI Team
    """)
