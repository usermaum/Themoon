import requests
import os
import json
import time

# Configuration
API_URL = "http://localhost:8000/api/v1/inbound"
IMAGE_PATH = r"d:\Ai\WslProject\TheMoon\.coffee_bean_receiving_Specification\명세서_1650.PNG"

def test_duplicate_prevention():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Image file not found at {IMAGE_PATH}")
        return

    print(f"1. Uploading {IMAGE_PATH}...")
    
    upload_data = {}
    try:
        with open(IMAGE_PATH, "rb") as f:
            files = {"file": (os.path.basename(IMAGE_PATH), f, "image/png")}
            response = requests.post(f"{API_URL}/upload", files=files)
            
        if response.status_code == 200:
            upload_data = response.json()
            print("✅ Upload Successful!")
            print(f"   Supplier: {upload_data.get('supplier_name')}")
            print(f"   Invoice No: {upload_data.get('invoice_number')}")
        else:
            print(f"❌ Upload Failed: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ Error during upload: {e}")
        return

    # Simulate manual entry of invoice number if OCR missed it
    if not upload_data.get('invoice_number'):
        upload_data['invoice_number'] = f"INV-{int(time.time())}"
        print(f"⚠️ OCR didn't find invoice number. Using generated: {upload_data['invoice_number']}")

    print("\n2. Confirming Inbound (First Time)...")
    try:
        response = requests.post(f"{API_URL}/confirm", json=upload_data)
        if response.status_code == 200:
            print("✅ Confirmation Successful!")
        else:
            print(f"❌ Confirmation Failed: {response.status_code}")
            print(response.text)
            return
    except Exception as e:
        print(f"❌ Error during confirmation: {e}")
        return

    print("\n3. Confirming Inbound (Duplicate Attempt)...")
    try:
        response = requests.post(f"{API_URL}/confirm", json=upload_data)
        if response.status_code == 400:
            print("✅ Duplicate Prevention Working! (Got 400 Bad Request)")
            print(f"   Message: {response.json().get('detail')}")
        else:
            print(f"❌ Duplicate Prevention Failed: Expected 400, got {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error during duplicate confirmation: {e}")

if __name__ == "__main__":
    test_duplicate_prevention()
