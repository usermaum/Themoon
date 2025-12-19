import requests
import json

API_URL = "http://localhost:8000/api/v1/inventory-logs"

def check_logs():
    try:
        response = requests.get(f"{API_URL}?limit=5")
        if response.status_code == 200:
            logs = response.json()
            print(f"Response Type: {type(logs)}")
            print(f"Raw Response: {json.dumps(logs, indent=2)}")
            
            items = logs if isinstance(logs, list) else logs.get('items', [])
            
            print(f"Found {len(items)} logs.")
            for log in items:
                print(f"ID: {log.get('id')}, Type: {log.get('transaction_type')}, Bean: {log.get('bean_id')}, Qty: {log.get('quantity_kg')}, Desc: {log.get('description')}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    check_logs()
