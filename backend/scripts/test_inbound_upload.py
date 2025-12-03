import requests
import os
import json

# Configuration
API_URL = "http://localhost:8000/api/v1/inbound/upload"
IMAGE_PATH = r"d:\Ai\WslProject\TheMoon\.coffee_bean_receiving_Specification\명세서_1650.PNG"

def test_upload():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Image file not found at {IMAGE_PATH}")
        return

    print(f"Uploading {IMAGE_PATH} to {API_URL}...")
    
    try:
        with open(IMAGE_PATH, "rb") as f:
            files = {"file": (os.path.basename(IMAGE_PATH), f, "image/png")}
            response = requests.post(API_URL, files=files)
            
        if response.status_code == 200:
            print("✅ Upload Successful!")
            print("Response Data:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print(f"❌ Upload Failed with status code: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error during request: {e}")

if __name__ == "__main__":
    test_upload()
