import sys
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.database import Base, get_db
from app.models.supplier import Supplier
from app.models.inbound_document import InboundDocument

# Test Database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_inbound.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create Tables
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_inbound_upgrade_flow():
    # Clear DB
    db = TestingSessionLocal()
    db.query(InboundDocument).delete()
    db.query(Supplier).delete()
    db.commit()
    db.close()

    payload = {
        "items": [
            {"bean_name": "Test Bean", "quantity": 10.0, "unit_price": 1000, "amount": 10000}
        ],
        "document": {
            "supplier_name": "Test Supplier Corp",
            "contract_number": "ORD-2025-0001",
            "supplier_phone": "010-1234-5678",
            "supplier_email": "test@corp.com",
            "receiver_name": "Manager Kim",
            "invoice_date": "2025-12-16",
            "total_amount": 10000,
            "notes": "Test Inbound"
        }
    }

    # 1. First Confirm (Success)
    print("Testing First Submission...")
    response = client.post("/api/v1/inbound/confirm", json=payload)
    assert response.status_code == 201, f"Failed: {response.text}"
    data = response.json()
    doc_id = data["document_id"]
    print(f" -> Success! Doc ID: {doc_id}")

    # Verify Supplier Created
    db = TestingSessionLocal()
    supplier = db.query(Supplier).filter(Supplier.name == "Test Supplier Corp").first()
    assert supplier is not None
    assert supplier.contact_phone == "010-1234-5678"
    print(f" -> Supplier Created: {supplier.name} (ID: {supplier.id})")
    
    # Verify Document
    doc = db.query(InboundDocument).filter(InboundDocument.id == doc_id).first()
    assert doc.contract_number == "ORD-2025-0001"
    assert doc.supplier_id == supplier.id
    print(f" -> Document Linked to Supplier: {doc.supplier_id}")
    db.close()

    # 2. Duplicate Confirm (Fail)
    print("Testing Duplicate Submission...")
    response_dup = client.post("/api/v1/inbound/confirm", json=payload)
    assert response_dup.status_code == 400
    assert "Duplicate Contract Number" in response_dup.text
    print(" -> Duplicate Check Passed!")

if __name__ == "__main__":
    try:
        test_inbound_upgrade_flow()
        print("\nALL TESTS PASSED ✅")
    except Exception as e:
        print(f"\nTEST FAILED ❌: {e}")
        sys.exit(1)
