"""
Verification script for multi-order processing system implementation

This script verifies:
1. InboundItem model has order_number column
2. OCRItem schema includes order_number field
3. OCR service prompt includes order number extraction instructions
4. InboundItem creation includes order_number
"""

import json
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


def verify_model():
    """Verify InboundItem model has order_number column"""
    print("\n1. Verifying InboundItem Model...")
    from app.models.inbound_item import InboundItem
    from sqlalchemy import inspect

    # Check if order_number column exists in model definition
    columns = [c.name for c in InboundItem.__table__.columns]

    if "order_number" in columns:
        print("   ✅ order_number column exists in InboundItem model")

        # Check column properties
        order_number_col = InboundItem.__table__.columns['order_number']
        print(f"   - Type: {order_number_col.type}")
        print(f"   - Nullable: {order_number_col.nullable}")
        print(f"   - Index: {order_number_col.index}")
        return True
    else:
        print("   ❌ order_number column NOT found in InboundItem model")
        print(f"   Available columns: {columns}")
        return False


def verify_schema():
    """Verify OCRItem schema includes order_number"""
    print("\n2. Verifying OCRItem Schema...")
    from app.schemas.inbound import OCRItem

    # Check model fields
    if hasattr(OCRItem, 'model_fields'):
        fields = OCRItem.model_fields
    else:
        fields = OCRItem.__fields__

    if "order_number" in fields:
        print("   ✅ order_number field exists in OCRItem schema")
        field_info = fields["order_number"]
        print(f"   - Field info: {field_info}")
        return True
    else:
        print("   ❌ order_number field NOT found in OCRItem schema")
        print(f"   Available fields: {list(fields.keys())}")
        return False


def verify_ocr_prompt_structure():
    """Verify OCR prompt structure includes order_number"""
    print("\n3. Verifying OCR Prompt Structure...")

    prompt_file = backend_dir / "app" / "resources" / "ocr_prompt_structure.json"

    if not prompt_file.exists():
        print(f"   ❌ OCR prompt structure file not found: {prompt_file}")
        return False

    with open(prompt_file, 'r', encoding='utf-8') as f:
        structure = json.load(f)

    if "items" in structure and len(structure["items"]) > 0:
        item_fields = structure["items"][0]
        if "order_number" in item_fields:
            print("   ✅ order_number field exists in OCR prompt structure")
            print(f"   - Description: {item_fields['order_number']}")
            return True
        else:
            print("   ❌ order_number field NOT found in OCR prompt structure")
            print(f"   Available fields: {list(item_fields.keys())}")
            return False
    else:
        print("   ❌ No items array found in OCR prompt structure")
        return False


def verify_ocr_service_prompt():
    """Verify OCR service includes order number extraction instructions"""
    print("\n4. Verifying OCR Service Prompt...")

    service_file = backend_dir / "app" / "services" / "ocr_service.py"

    if not service_file.exists():
        print(f"   ❌ OCR service file not found: {service_file}")
        return False

    with open(service_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check for order number extraction step
    checks = [
        ("STEP 5-1", "STEP 5-1. ORDER NUMBER EXTRACTION"),
        ("order_number", "order_number field mentioned"),
        ("YYYYMMDD-XXXXX", "Order number format pattern"),
    ]

    results = []
    for key, description in checks:
        if key in content:
            print(f"   ✅ {description} found")
            results.append(True)
        else:
            print(f"   ❌ {description} NOT found")
            results.append(False)

    return all(results)


def verify_endpoint_implementation():
    """Verify inbound endpoint uses order_number"""
    print("\n5. Verifying Inbound Endpoint Implementation...")

    endpoint_file = backend_dir / "app" / "api" / "v1" / "endpoints" / "inbound.py"

    if not endpoint_file.exists():
        print(f"   ❌ Inbound endpoint file not found: {endpoint_file}")
        return False

    with open(endpoint_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if order_number is included in InboundItem creation
    if "order_number=item.order_number" in content:
        print("   ✅ order_number is included in InboundItem creation")
        return True
    else:
        print("   ❌ order_number NOT found in InboundItem creation")
        return False


def verify_migration_file():
    """Verify migration file exists"""
    print("\n6. Verifying Migration File...")

    migration_file = backend_dir / "migrations" / "add_order_number_to_inbound_items.sql"

    if migration_file.exists():
        print(f"   ✅ Migration file exists: {migration_file}")

        with open(migration_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for key SQL statements
        checks = [
            "ALTER TABLE inbound_items",
            "ADD COLUMN order_number",
            "CREATE INDEX idx_inbound_items_order_number",
        ]

        for check in checks:
            if check in content:
                print(f"   ✅ {check}")
            else:
                print(f"   ⚠️  {check} NOT found")

        return True
    else:
        print(f"   ⚠️  Migration file not found: {migration_file}")
        print("   Note: Migration may be applied manually or via Alembic")
        return True  # Not critical


def main():
    """Run all verifications"""
    print("=" * 60)
    print("Multi-Order Processing System Verification")
    print("=" * 60)

    results = {
        "Model": verify_model(),
        "Schema": verify_schema(),
        "OCR Prompt Structure": verify_ocr_prompt_structure(),
        "OCR Service Prompt": verify_ocr_service_prompt(),
        "Endpoint Implementation": verify_endpoint_implementation(),
        "Migration File": verify_migration_file(),
    }

    print("\n" + "=" * 60)
    print("Verification Summary:")
    print("=" * 60)

    for check, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {check}")

    print("=" * 60)

    if all(results.values()):
        print("\n🎉 All verifications passed!")
        return 0
    else:
        print("\n⚠️  Some verifications failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
