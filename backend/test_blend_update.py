import requests
import json

base_url = "http://localhost:8000/api/v1"

try:
    # 1. 블렌드 조회
    print("Fetching blend #1...")
    res = requests.get(f"{base_url}/blends/1")
    if res.status_code != 200:
        print(f"❌ Failed to fetch blend: {res.text}")
        exit()
    
    blend = res.json()
    print(f"Current Blend: {blend['name']}")
    
    # 2. 업데이트 데이터 준비 (기존 데이터 유지하고 설명만 변경)
    update_data = {
        "name": blend['name'],
        "description": blend['description'] + " (Updated)",
        "target_roast_level": blend['target_roast_level'],
        "notes": blend['notes'],
        "recipe": blend['recipe']  # 기존 레시피 그대로 전송
    }
    
    # 3. 업데이트 요청
    print("Attempting to update blend #1...")
    res = requests.put(f"{base_url}/blends/1", json=update_data)
    
    print(f"Status Code: {res.status_code}")
    print(f"Response Body: {res.text}")

except Exception as e:
    print(f"❌ Error: {e}")
