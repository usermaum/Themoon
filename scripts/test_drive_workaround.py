import sys
import os
import io
from googleapiclient.http import MediaIoBaseUpload

# Add backend directory to sys.path definitions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.google_drive_service import GoogleDriveService

TARGET_EMAIL = "usermaum@gmail.com"

def test_workaround():
    print("🧪 Starting Advanced Workaround Test...")
    print(f"🎯 Target Owner: {TARGET_EMAIL}")
    
    try:
        drive = GoogleDriveService()
        if not drive.service:
            print("❌ Service not initialized")
            return

        # 1. Find Folder
        folder_id = drive.find_folder_id("TheMoon_Inbound")
        if not folder_id:
            print("❌ Folder 'TheMoon_Inbound' not found. Please create it and share it.")
            return
        print(f"bm Folder ID: {folder_id}")

        # 2. Create Metadata Only (No Media)
        print("📂 Creating file metadata (no content)...")
        file_metadata = {
            'name': 'workaround_test_file.txt',
            'parents': [folder_id],
            'mimeType': 'text/plain'
        }
        
        file = drive.service.files().create(
            body=file_metadata,
            fields='id',
            supportsAllDrives=True
        ).execute()
        
        file_id = file.get('id')
        print(f"✅ Metadata created! File ID: {file_id}")

        # 3. Attempt Ownership Transfer
        print("👤 Attempting to transfer ownership request...")
        # Note: Ownership transfer directly via API for personal accounts/consumer to/from SA is often restricted.
        # usually permissions.create with role='owner', transferOwnership=true
        
        try:
            permission_body = {
                'role': 'owner',
                'type': 'user',
                'emailAddress': TARGET_EMAIL
            }
            # Note: transferOwnership=True is required for transferring ownership
            drive.service.permissions().create(
                fileId=file_id,
                body=permission_body,
                transferOwnership=True,
                fields='id'
            ).execute()
            print("✅ Ownership transfer initiated/completed!")
        except Exception as e:
            print(f"❌ Ownership transfer failed: {e}")
            print("⚠️ Cannot proceed with content upload if ownership is not transferred (quota remains with SA).")
            # We will try to content upload anyway just to see
            
        # 4. Upload Content
        print("📝 Attempting to upload content...")
        media = MediaIoBaseUpload(io.BytesIO(b"Hello World"), mimetype='text/plain', resumable=True)
        
        drive.service.files().update(
            fileId=file_id,
            media_body=media,
            fields='identicon',
            supportsAllDrives=True
        ).execute()
        print("✅ Content uploaded successfully!")

    except Exception as e:
        print(f"❌ Test Failed: {e}")

if __name__ == "__main__":
    test_workaround()
