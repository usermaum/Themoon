import sys
import os

# Add backend directory to sys.path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.google_drive_service import GoogleDriveService

def test_drive_upload():
    print("🚀 Starting Google Drive Upload Test...")
    
    # Path to the test image provided by the user
    image_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public', 'inventory_hero_bg.png')
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found at {image_path}")
        return

    print(f"📄 Found test image: {image_path}")
    
    try:
        # Initialize Service
        print("🔧 Initializing GoogleDriveService...")
        drive_service = GoogleDriveService()
        
        if not drive_service.service:
            print("❌ Failed to initialize Google Drive Service (Check credentials).")
            return

        # Read image
        print("📖 Reading image file...")
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        print(f"📦 Image size: {len(image_bytes)} bytes")

        # Upload
        print("☁️ Attempting upload to 'TheMoon_Inbound' folder...")
        link = drive_service.upload_file(image_bytes, "test_upload_inventory_hero.png", "TheMoon_Inbound")
        
        print("\n✅ Upload Successful!")
        print(f"🔗 File Link: {link}")

    except Exception as e:
        print("\n❌ Upload Failed!")
        print(f"⚠️ Error Details: {e}")

if __name__ == "__main__":
    test_drive_upload()
