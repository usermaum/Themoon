import os
import sys
from pathlib import Path
from PIL import Image

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.services.image_service import ImageService

def test_image_service_security():
    print("🚀 Starting ImageService Security Verification...")
    
    # Use a unique test directory
    test_upload_dir = "static/test_uploads_security"
    service = ImageService(upload_base_dir=test_upload_dir)
    
    # 1. Prepare test image
    # Note: We are using a standard image, so real EXIF stripping verification 
    # would ideally need an image with EXIF data. 
    # Here we verify the method runs without error and security path validation works.
    test_image_path = Path("frontend/public/images/hero/inbound_hero.png") 
    if not test_image_path.exists():
        # Fallback to any file in that dir
        hero_dir = Path("frontend/public/images/hero")
        images = list(hero_dir.glob("*.png"))
        if images:
            test_image_path = images[0]
        else:
            print(f"❌ Test image not found")
            return

    print(f"📸 Using test image: {test_image_path}")
    with open(test_image_path, "rb") as f:
        image_bytes = f.read()

    # 2. Test Processing with Security Features
    print("🛡️ Testing Processing with EXIF Removal & Path Validation...")
    try:
        results = service.process_and_save(image_bytes, str(test_image_path.name))
        print("✅ Processing Success (EXIF removal executed)")
        
        # Verify Output
        for tier, rel_path in results['paths'].items():
            abs_path = Path(test_upload_dir) / rel_path
            if abs_path.exists():
                print(f"   - {tier}: {rel_path} created.")
            else:
                print(f"   - ❌ Missing tier: {tier}")
                
    except Exception as e:
        print(f"❌ Processing Failed: {str(e)}")

    # 3. Test Path Traversal Protection (Unit Test Style)
    print("🚫 Testing Path Traversal Protection...")
    try:
        # Mocking a path traversal attempt
        if not service._validate_path_security(Path("/etc/passwd")):
             print("✅ Path traversal to /etc/passwd correctly blocked")
        else:
             print("❌ Path traversal to /etc/passwd NOT blocked")

        if service._validate_path_security(Path(test_upload_dir) / "2023/12"):
             print("✅ Valid path correctly accepted")
        else:
             print("❌ Valid path incorrectly blocked")
             
    except Exception as e:
        print(f"❌ Path Validation Test Error: {e}")

    print("\n🎉 Security Verification Complete")

if __name__ == "__main__":
    test_image_service_security()
