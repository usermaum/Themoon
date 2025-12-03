import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def verify_dashboard():
    print("Verifying Dashboard API...")

    # 1. Get Stats
    print("\n1. Testing /stats...")
    r1 = requests.get(f"{BASE_URL}/dashboard/stats")
    if r1.status_code == 200:
        print("✅ Stats:", json.dumps(r1.json(), indent=2))
    else:
        print(f"❌ Stats failed: {r1.text}")

    # 2. Get Low Stock
    print("\n2. Testing /low-stock...")
    r2 = requests.get(f"{BASE_URL}/dashboard/low-stock?threshold=1000") # High threshold to ensure results
    if r2.status_code == 200:
        print("✅ Low Stock:", json.dumps(r2.json()[:2], indent=2)) # Show first 2
    else:
        print(f"❌ Low Stock failed: {r2.text}")

    # 3. Get Recent Activity
    print("\n3. Testing /recent-activity...")
    r3 = requests.get(f"{BASE_URL}/dashboard/recent-activity")
    if r3.status_code == 200:
        print("✅ Recent Activity:", json.dumps(r3.json()[:2], indent=2)) # Show first 2
    else:
        print(f"❌ Recent Activity failed: {r3.text}")

if __name__ == "__main__":
    verify_dashboard()
