"""
사용 가능한 Gemini 모델 목록 확인
"""

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

print("=" * 60)
print("사용 가능한 Gemini 모델 목록")
print("=" * 60)

try:
    models = client.models.list()
    for model in models:
        print(f"- {model.name}")
        if hasattr(model, 'display_name'):
            print(f"  Display Name: {model.display_name}")
        if hasattr(model, 'supported_generation_methods'):
            print(f"  Supported Methods: {model.supported_generation_methods}")
        print()
except Exception as e:
    print(f"오류: {e}")
