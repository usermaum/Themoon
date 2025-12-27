import requests
import json

API_URL = "http://localhost:8000/api/v1/suppliers"

def check_suppliers():
    try:
        response = requests.get(f"{API_URL}?limit=100")
        if response.status_code == 200:
            suppliers = response.json()
            print(f"Response Type: {type(suppliers)}")
            
            items = suppliers if isinstance(suppliers, list) else suppliers.get('items', [])
            
            print(f"Found {len(items)} suppliers.")
            names = [s.get('name') for s in items]
            print(f"Names: {names}")
            
            # Check for potential duplicates (simple similarity)
            seen = set()
            duplicates = []
            for name in names:
                if name in seen:
                    duplicates.append(name)
                seen.add(name)
            
            if duplicates:
                print(f"⚠️ Exact Duplicates found: {duplicates}")
            else:
                print("✅ No exact duplicates found.")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_suppliers()
