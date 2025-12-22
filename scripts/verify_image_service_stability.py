import os
import sys
import shutil
from pathlib import Path
from PIL import Image

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.services.image_service import ImageService

def test_image_service_stability():
    print("🚀 Starting ImageService Stability Verification...")
    
    # Use a unique test directory
    test_upload_dir = "static/test_uploads_stability"
    # Ensure clean start
    if os.path.exists(test_upload_dir):
        shutil.rmtree(test_upload_dir)
    
    service = ImageService(upload_base_dir=test_upload_dir)
    
    # 1. Prepare test image
    test_image_path = Path("frontend/public/images/hero/inbound_hero.png") 
    if not test_image_path.exists():
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

    # 2. Test Disk Space Check
    print("\n💾 Testing Disk Space Check...")
    try:
        # Mock disk usage to return low space (1GB free)
        original_disk_usage = shutil.disk_usage
        def mock_disk_usage(path):
            return shutil._ntuple_diskusage(100 * 1024**3, 99 * 1024**3, 1 * 1024**3) # total, used, free
        
        shutil.disk_usage = mock_disk_usage
        
        try:
            service.process_and_save(image_bytes, "test_disk_full.jpg")
            print("❌ Disk space check FAILED (Should have raised IOError)")
        except IOError as e:
            if "Insufficient disk space" in str(e):
                print("✅ Disk space check PASSED (Correctly raised IOError)")
            else:
                print(f"❌ Unexpected IOError: {e}")
        except Exception as e:
            print(f"❌ Unexpected error type: {type(e)}")

    finally:
        # Restore original function
        shutil.disk_usage = original_disk_usage


    # 3. Test Atomic Save & Partial Cleanup
    print("\n⚛️ Testing Atomic Save & Partial Cleanup...")
    
    # We will simulate a failure during the saving of the 2nd tier (webview)
    # to see if the 1st tier (original) is cleaned up.
    
    original_save_atomic = service._save_atomic
    save_call_count = 0
    
    def mock_save_atomic_fail_on_second(img, target_path, **kwargs):
        nonlocal save_call_count
        save_call_count += 1
        if save_call_count == 2:
            raise RuntimeError("Simulated Save Failure on 2nd Tier")
        return original_save_atomic(img, target_path, **kwargs)

    service._save_atomic = mock_save_atomic_fail_on_second
    
    try:
        service.process_and_save(image_bytes, "test_rollback.jpg")
        print("❌ Rollback test FAILED (Should have raised RuntimeError)")
    except RuntimeError as e:
        print("✅ Simulated failure caught")
        
        # Verify cleanup
        # 'original' should have been saved (call 1), then cleanup should have deleted it
        # because the process failed on call 2.
        
        # We need to check if ANY files remain in the target directory for this specific file
        # Since we don't know the exact random filename, we check the directory.
        # But wait, the directories are by date.
        
        # Let's check the test_upload_dir recursively.
        files_found = list(Path(test_upload_dir).rglob("*test_rollback*"))
        remaining_files = [f for f in files_found if f.is_file()]
        
        if len(remaining_files) == 0:
            print("✅ Cleanup PASSED (No partial files remaining)")
        else:
            print(f"❌ Cleanup FAILED. Remaining files: {remaining_files}")
            
    finally:
        service._save_atomic = original_save_atomic

    print("\n🎉 Stability Verification Complete")

if __name__ == "__main__":
    test_image_service_stability()
