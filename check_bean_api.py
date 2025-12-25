import requests
import sys
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_bean_crud():
    print("Testing Bean API CRUD operations...")
    
    # 1. List Beans
    try:
        response = requests.get(f"{BASE_URL}/beans/")
        response.raise_for_status()
        beans = response.json()
        print(f"✅ List Beans: Success (Count: {beans['total']})")
    except Exception as e:
        print(f"❌ List Beans: Failed - {e}")
        return False

    # 2. Create Bean
    new_bean_data = {
        "name": "Test Bean Refactor",
        "type": "GREEN_BEAN",
        "origin": "Test Origin",
        "quantity_kg": 10.0,
        "avg_price": 100.0
    }
    created_bean_id = None
    try:
        response = requests.post(f"{BASE_URL}/beans/", json=new_bean_data)
        response.raise_for_status()
        created_bean = response.json()
        created_bean_id = created_bean["id"]
        print(f"✅ Create Bean: Success (ID: {created_bean_id})")
    except Exception as e:
        print(f"❌ Create Bean: Failed - {e}")
        return False

    if not created_bean_id:
        return False

    # 3. Update Bean
    update_data = {"notes": "Updated by verification script"}
    try:
        response = requests.put(f"{BASE_URL}/beans/{created_bean_id}", json=update_data)
        response.raise_for_status()
        updated_bean = response.json()
        if updated_bean["notes"] == "Updated by verification script":
             print(f"✅ Update Bean: Success")
        else:
             print(f"❌ Update Bean: Failed (Content mismatch)")
    except Exception as e:
        print(f"❌ Update Bean: Failed - {e}")
        # Clean up even if update failed
        requests.delete(f"{BASE_URL}/beans/{created_bean_id}")
        return False

    # 4. Delete Bean
    try:
        response = requests.delete(f"{BASE_URL}/beans/{created_bean_id}")
        response.raise_for_status()
        print(f"✅ Delete Bean: Success")
    except Exception as e:
        print(f"❌ Delete Bean: Failed - {e}")
        return False

    # 5. Verify Deletion
    try:
        response = requests.get(f"{BASE_URL}/beans/{created_bean_id}")
        if response.status_code == 404:
            print(f"✅ Verify Deletion: Success (404 returned)")
        else:
            print(f"❌ Verify Deletion: Failed (Status {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Verify Deletion: Failed - {e}")
        return False

    return True

if __name__ == "__main__":
    if test_bean_crud():
        print("\n🎉 All Bean API tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Some Bean API tests failed.")
        sys.exit(1)
