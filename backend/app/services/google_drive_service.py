import os
import io
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive']

class GoogleDriveService:
    def __init__(self):
        self.creds = None
        self.service = None
        self._authenticate()

    def _authenticate(self):
        service_account_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", ".gemini/service_account.json")
        
        # Check if path is absolute or relative
        if not os.path.isabs(service_account_path):
            # Assume relative to project root (backend's parent)
            # backend/app/services -> backend/app -> backend -> root
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            # Adjust if we are in backend dir context
            # Let's try to find it relative to current working directory (usually root in dev)
            if os.path.exists(service_account_path):
                pass 
            elif os.path.exists(os.path.join("..", service_account_path)):
                 service_account_path = os.path.join("..", service_account_path)
        
        if os.path.exists(service_account_path):
            self.creds = service_account.Credentials.from_service_account_file(
                service_account_path, scopes=SCOPES
            )
            self.service = build('drive', 'v3', credentials=self.creds)
        else:
            print(f"Warning: Service account file not found at {service_account_path}")

    def find_folder_id(self, folder_name: str) -> Optional[str]:
        if not self.service:
            return None
        
        query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and trashed=false"
        # CHANGED: Added support for Shared Drives
        results = self.service.files().list(
            q=query, 
            fields="files(id, name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True
        ).execute()
        files = results.get('files', [])
        
        if files:
            return files[0]['id']
        return None

    def create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        if not self.service:
            raise Exception("Google Drive Service not initialized")

        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        if parent_id:
            file_metadata['parents'] = [parent_id]
            
        file = self.service.files().create(
            body=file_metadata, 
            fields='id',
            supportsAllDrives=True
        ).execute()
        return file.get('id')

    def upload_file(self, file_content: bytes, filename: str, folder_name: str = "TheMoon_Inbound") -> str:
        """
        Uploads a file to Google Drive and returns the webViewLink.
        """
        if not self.service:
            raise Exception("Google Drive Service not initialized")

        # 1. Find or Create Folder
        folder_id = self.find_folder_id(folder_name)
        if not folder_id:
            folder_id = self.create_folder(folder_name)

        # 2. Upload File
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        
        media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype='image/jpeg', resumable=True)
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink, webContentLink',
            supportsAllDrives=True
        ).execute()

        # 3. Create Permission (Public Reader - or rely on Service Account access)
        # To make it viewable by the user, we might need to share it or return a link that works if the folder is shared.
        # Since the folder is shared with the service account, files created by SA are owned by SA.
        # To make them visible to the user who owns the folder, the folder ownership flows down usually, 
        # but files created by SA might strictly belong to SA unless ownership is transferred or permissions added.
        # But if the folder is shared *with* SA, the SA is an editor.
        # Let's ensure the file is readable by anyone with the link (or just the domain) if needed, 
        # BUT the safely is restricted to the folder permissions. 
        # If the user shared the folder with the SA, the user can see files inside it.
        
        return file.get('webViewLink')
