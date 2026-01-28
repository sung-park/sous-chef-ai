"""
chef_brain.py 테스트 스크립트
RecipeAgent의 generate_recipe 메서드를 테스트합니다.
"""

import json
from chef_brain import RecipeAgent


def test_generate_recipe():
    """
    김치찌개 레시피 생성 테스트
    """
    print("=" * 60)
    print("🧪 RecipeAgent 테스트 시작")
    print("=" * 60)
    print()

    # RecipeAgent 초기화
    try:
        agent = RecipeAgent()
        print("✅ RecipeAgent 초기화 성공")
        print()
    except Exception as e:
        print(f"❌ RecipeAgent 초기화 실패: {e}")
        return

    # 김치찌개 레시피 생성
    dish_name = "김치찌개"
    print(f"🍲 요리명: {dish_name}")
    print(f"📡 Gemini API 호출 중...")
    print()

    try:
        recipe = agent.generate_recipe(dish_name)
        print("✅ 레시피 생성 성공!")
        print()

        # 결과 출력
        print("=" * 60)
        print("📋 생성된 레시피 (JSON)")
        print("=" * 60)
        print(json.dumps(recipe, ensure_ascii=False, indent=2))
        print()

        # 구조 검증
        print("=" * 60)
        print("🔍 JSON 구조 검증")
        print("=" * 60)

        required_keys = ["title", "cooking_time", "ingredients", "steps"]
        all_keys_present = all(key in recipe for key in required_keys)

        if all_keys_present:
            print("✅ 모든 필수 키가 존재합니다.")
            print(f"  - title: {recipe['title']}")
            print(f"  - cooking_time: {recipe['cooking_time']}")
            print(f"  - ingredients: {len(recipe['ingredients'])}개")
            print(f"  - steps: {len(recipe['steps'])}단계")
        else:
            print("❌ 필수 키가 누락되었습니다.")
            missing_keys = [key for key in required_keys if key not in recipe]
            print(f"  누락된 키: {missing_keys}")

        print()

        # 상세 내용 출력
        print("=" * 60)
        print("🍳 레시피 상세 내용")
        print("=" * 60)
        print(f"\n📌 {recipe['title']}")
        print(f"⏱️  소요 시간: {recipe['cooking_time']}")
        print()

        print("🥘 재료:")
        for i, ingredient in enumerate(recipe['ingredients'], 1):
            print(f"  {i}. {ingredient}")
        print()

        print("👨‍🍳 조리 과정:")
        for i, step in enumerate(recipe['steps'], 1):
            print(f"  {i}. {step}")
        print()

    except Exception as e:
        print(f"❌ 레시피 생성 실패: {e}")
        import traceback
        traceback.print_exc()

    print("=" * 60)
    print("🧪 테스트 완료")
    print("=" * 60)


if __name__ == "__main__":
    test_generate_recipe()
