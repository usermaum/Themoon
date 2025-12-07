import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint(endpoint):
    print(f"\nTesting GET {endpoint}...")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response Data Sample (First item or keys):")
            
            if isinstance(data, list):
                print(f"✅ Received List with {len(data)} items.")
                if len(data) > 0:
                    print(json.dumps(data[0], indent=2, ensure_ascii=False))
            elif isinstance(data, dict):
                print(f"✅ Received Dict keys: {list(data.keys())}")
                if "items" in data and len(data["items"]) > 0:
                     print(json.dumps(data["items"][0], indent=2, ensure_ascii=False))
            else:
                print(data)
        else:
            print(f"❌ Error Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_endpoint("/beans")
    test_endpoint("/inventory-logs")
