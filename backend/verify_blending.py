import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def create_test_data():
    print("Creating test data...")
    # 1. Create Ingredients
    brazil = {
        "name": "Brazil Santos Test",
        "type": "GREEN_BEAN",
        "origin": "Brazil",
        "quantity_kg": 100.0,
        "avg_cost_price": 10000.0
    }
    colombia = {
        "name": "Colombia Supremo Test",
        "type": "GREEN_BEAN",
        "origin": "Colombia",
        "quantity_kg": 100.0,
        "avg_cost_price": 15000.0
    }
    
    r1 = requests.post(f"{BASE_URL}/beans/", json=brazil)
    r2 = requests.post(f"{BASE_URL}/beans/", json=colombia)
    
    if r1.status_code != 201 or r2.status_code != 201:
        print(f"Failed to create ingredients. R1: {r1.status_code} {r1.text}, R2: {r2.status_code} {r2.text}")
        return None
        
    b1 = r1.json()
    b2 = r2.json()
    print(f"Created ingredients: {b1['name']}, {b2['name']}")
    
    # 2. Create Blend Recipe
    blend_data = {
        "name": "Test Full Moon Blend",
        "recipe": [
            {"bean_id": b1['id'], "ratio": 0.6},
            {"bean_id": b2['id'], "ratio": 0.4}
        ],
        "target_roast_level": "Medium"
    }
    
    r3 = requests.post(f"{BASE_URL}/blends/", json=blend_data)
    if r3.status_code != 201:
        print(f"Failed to create blend: {r3.text}")
        return None
        
    blend = r3.json()
    print(f"Created blend: {blend['name']}")
    return blend

def verify_blending():
    # 1. Get Blends
    print("Fetching blends...")
    response = requests.get(f"{BASE_URL}/blends/")
    blends = response.json()
    
    target_blend = None
    if not blends:
        print("No blends found. Creating test data...")
        target_blend = create_test_data()
    else:
        # Try to find our test blend
        for b in blends:
            if "Test" in b['name']:
                target_blend = b
                break
        
        if not target_blend:
             print("Test blend not found. Creating test data...")
             target_blend = create_test_data()

    if not target_blend:
        print("Could not get a target blend.")
        return

    print(f"Target Blend: {target_blend['name']} (ID: {target_blend['id']})")
    
    # 3. Produce Blend
    print(f"Attempting to produce 10kg of {target_blend['name']}...")
    payload = {
        "blend_id": target_blend['id'],
        "amount_kg": 10.0
    }
    
    response = requests.post(f"{BASE_URL}/blends/production", json=payload)
    
    if response.status_code == 200:
        print("✅ Production successful!")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"❌ Production failed: {response.text}")

if __name__ == "__main__":
    verify_blending()
