#!/usr/bin/env python3
"""Bean API 테스트 스크립트"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_bean_filter():
    """Bean type 필터 테스트"""

    print("=" * 60)
    print("1. 전체 조회 (필터 없음)")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/api/v1/beans/?page=1&size=5")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total: {data['total']}")
    print(f"Types: {[item['type'] for item in data['items']]}")
    print()

    print("=" * 60)
    print("2. GREEN_BEAN 필터")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/api/v1/beans/?page=1&size=5&type=GREEN_BEAN")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total: {data['total']}")
    print(f"Types: {[item['type'] for item in data['items']]}")
    print()

    print("=" * 60)
    print("3. ROASTED_BEAN 필터")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/api/v1/beans/?page=1&size=5&type=ROASTED_BEAN")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total: {data['total']}")
    if data['items']:
        print(f"Types: {[item['type'] for item in data['items']]}")
        print(f"Names: {[item['name'] for item in data['items']]}")
    else:
        print("No items returned")
    print()

    print("=" * 60)
    print("4. BLEND_BEAN 필터")
    print("=" * 60)
    response = requests.get(f"{BASE_URL}/api/v1/beans/?page=1&size=5&type=BLEND_BEAN")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total: {data['total']}")
    print(f"Types: {[item['type'] for item in data['items']]}")
    print()

if __name__ == "__main__":
    test_bean_filter()
