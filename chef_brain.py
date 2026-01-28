from google import genai
from google.genai import types
import os
import json
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()


class RecipeAgent:
    """
    AI 셰프 에이전트: Gemini를 활용한 레시피 생성 및 이미지 생성
    """

    def __init__(self):
        """
        RecipeAgent 초기화
        - Gemini API 설정
        """
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY가 .env 파일에 설정되지 않았습니다.")

        # Gemini Client 생성
        self.client = genai.Client(api_key=api_key)

        # 모델 이름
        self.model_name = "gemini-2.5-flash"

        # 시스템 프롬프트
        self.system_prompt = """
너는 20년 경력의 셰프이자 파워 블로거야.
친절하고 감성적인 말투로 레시피를 작성해줘.
각 단계마다 요리 팁이나 포인트를 자연스럽게 녹여서 설명해줘.
"""

    def generate_recipe(self, dish_name: str) -> dict:
        """
        요리명을 받아서 Gemini로 레시피를 생성

        Args:
            dish_name: 요리 이름

        Returns:
            dict: 레시피 정보 (제목, 소요시간, 재료, 조리과정)
        """

        # 프롬프트 구성
        prompt = f"""
{self.system_prompt}

요리명: {dish_name}

위 요리에 대한 레시피를 아래 JSON 형식으로 작성해줘.
반드시 유효한 JSON 형식으로만 답변해줘. 다른 설명은 붙이지 말고 오직 JSON만 출력해.

{{
  "title": "요리 제목 (감성적으로)",
  "cooking_time": "소요 시간 (예: 30분)",
  "ingredients": [
    "재료1 (양)",
    "재료2 (양)",
    "재료3 (양)"
  ],
  "steps": [
    "1단계: 구체적인 조리 방법과 팁",
    "2단계: 구체적인 조리 방법과 팁",
    "3단계: 구체적인 조리 방법과 팁",
    "4단계: 구체적인 조리 방법과 팁",
    "5단계: 구체적인 조리 방법과 팁"
  ]
}}
"""

        try:
            # Gemini API 호출
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                )
            )

            # 응답 텍스트 추출
            response_text = response.text.strip()

            # JSON 파싱
            # Gemini가 가끔 ```json ``` 로 감싸서 반환할 수 있으므로 처리
            if response_text.startswith("```json"):
                response_text = response_text[7:]  # ```json 제거
            if response_text.startswith("```"):
                response_text = response_text[3:]  # ``` 제거
            if response_text.endswith("```"):
                response_text = response_text[:-3]  # ``` 제거

            response_text = response_text.strip()

            # JSON 파싱
            recipe_data = json.loads(response_text)

            return recipe_data

        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            print(f"응답 내용:\n{response_text}")
            raise
        except Exception as e:
            print(f"레시피 생성 중 오류 발생: {e}")
            raise

    def generate_image(self, dish_name: str, recipe_data: dict) -> str:
        """
        요리 이미지 생성 (Imagen 3 사용 예정)

        Args:
            dish_name: 요리 이름
            recipe_data: 레시피 데이터

        Returns:
            str: 생성된 이미지 URL 또는 경로
        """
        # TODO: Imagen 3 API 연동 예정
        pass
