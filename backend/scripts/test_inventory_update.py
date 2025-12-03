import requests
import json
import os

API_URL = "http://localhost:8000/api/v1"
# Use an existing bean ID. Based on init_data.py, ID 1 should exist.
BEAN_ID = 1

def get_bean_stock(bean_id):
    response = requests.get(f"{API_URL}/beans/{bean_id}")
    if response.status_code == 200:
        data = response.json()
        return data['quantity_kg'], data['avg_cost_price']
    return None, None

def verify_inventory_update():
    print(f"Checking initial stock for Bean ID {BEAN_ID}...")
    initial_qty, initial_price = get_bean_stock(BEAN_ID)
    if initial_qty is None:
        print("❌ Failed to fetch bean data.")
        return

    print(f"Initial Stock: {initial_qty} kg, Avg Price: {initial_price}")

    # Simulate Inbound Confirmation with a matched item
    # We skip the upload step and directly call confirm with a constructed payload
    # assuming the file path exists or we use a dummy path (backend might check existence, but let's try)
    
    # Note: The backend checks if file exists? 
    # InboundDocument creation uses file_path. 
    # Let's use a dummy path or a real one if needed. 
    # The confirm endpoint doesn't strictly validate file existence on disk for logic, just saves the path.
    
    payload = {
        "supplier_name": "Test Supplier",
        "invoice_number": f"TEST-INV-{os.urandom(4).hex()}",
        "date": "2023-12-03",
        "total_amount": 100000,
        "items": [
            {
                "name": "Test Bean Item",
                "quantity": 10.0,
                "unit_price": 10000.0,
                "total_price": 100000.0,
                "matched_bean_id": BEAN_ID
            }
        ],
        "temp_file_path": "uploads/dummy_test_file.png" 
    }

    print("\nConfirming Inbound Transaction...")
    response = requests.post(f"{API_URL}/inbound/confirm", json=payload)
    
    if response.status_code != 200:
        print(f"❌ Confirmation Failed: {response.status_code}")
        print(response.text)
        return

    print("✅ Confirmation Successful!")

    print(f"\nChecking updated stock for Bean ID {BEAN_ID}...")
    final_qty, final_price = get_bean_stock(BEAN_ID)
    
    print(f"Final Stock: {final_qty} kg, Avg Price: {final_price}")
    
    expected_qty = initial_qty + 10.0
    if final_qty == expected_qty:
        print(f"✅ Stock updated correctly! ({initial_qty} -> {final_qty})")
    else:
        print(f"❌ Stock mismatch! Expected {expected_qty}, got {final_qty}")

if __name__ == "__main__":
    verify_inventory_update()
