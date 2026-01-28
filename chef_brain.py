from google import genai
from google.genai import types
import os
import json
import base64
from pathlib import Path
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

    def generate_image(self, prompt: str, dish_name: str = "dish") -> str:
        """
        Imagen을 사용해서 요리 이미지 생성

        Args:
            prompt: 이미지 생성 프롬프트
            dish_name: 요리 이름 (파일명에 사용)

        Returns:
            str: 생성된 이미지 파일 경로
        """
        try:
            # temp 폴더 생성 (없으면)
            temp_dir = Path("temp")
            temp_dir.mkdir(exist_ok=True)

            # 이미지 생성 프롬프트 (영어로 번역)
            image_prompt = f"A professional food photography of {prompt}, beautifully plated, appetizing, high quality, restaurant style"

            print(f"🎨 이미지 생성 프롬프트: {image_prompt}")

            # Imagen 4 모델 사용
            response = self.client.models.generate_images(
                model="imagen-4.0-generate-001",
                prompt=image_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="1:1",
                )
            )

            # 생성된 이미지 추출
            if response.generated_images:
                generated_image = response.generated_images[0]

                # 이미지 데이터를 파일로 저장
                # dish_name에서 특수문자 제거
                safe_dish_name = "".join(c for c in dish_name if c.isalnum() or c in (' ', '_')).strip()
                safe_dish_name = safe_dish_name.replace(' ', '_')

                image_path = temp_dir / f"{safe_dish_name}_image.png"

                # 이미지 데이터 저장
                # PIL Image 객체인 경우
                if hasattr(generated_image, 'save'):
                    # PIL Image 객체인 경우 save 메서드 사용
                    generated_image.save(image_path)
                elif hasattr(generated_image, 'image'):
                    # image 속성이 있는 경우
                    image_data = generated_image.image
                    if hasattr(image_data, 'save'):
                        # PIL Image 객체
                        image_data.save(image_path)
                    elif isinstance(image_data, str):
                        # base64 인코딩된 문자열인 경우
                        image_bytes = base64.b64decode(image_data)
                        with open(image_path, 'wb') as f:
                            f.write(image_bytes)
                    elif isinstance(image_data, bytes):
                        # 이미 bytes인 경우
                        with open(image_path, 'wb') as f:
                            f.write(image_data)
                elif hasattr(generated_image, 'bytes'):
                    # bytes 속성이 있는 경우
                    with open(image_path, 'wb') as f:
                        f.write(generated_image.bytes)
                else:
                    raise Exception(f"알 수 없는 이미지 형식: {type(generated_image)}")

                print(f"✅ 이미지 저장 완료: {image_path}")
                return str(image_path)
            else:
                raise Exception("이미지가 생성되지 않았습니다.")

        except Exception as e:
            print(f"❌ 이미지 생성 중 오류 발생: {e}")
            raise
