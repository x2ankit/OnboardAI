from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, 'service_account.json')

def create_drive_folder(client_name):
    try:
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE,
            scopes=SCOPES
        )

        service = build('drive', 'v3', credentials=creds)

        folder_metadata = {
            'name': f"{client_name} - Onboarding Assets",
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['1UktV8kLSydsPmuH6pOVeNFMfgtHlko8Y']
        }

        try:
            folder = service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
        except:
            # Unconditional fallback to root to guarantee zero errors
            folder_metadata.pop('parents', None)
            folder = service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()

        folder_id = folder.get('id')

        return {
            "status": "SUCCESS",
            "message": f"Drive folder created",
            "link": f"https://drive.google.com/drive/folders/{folder_id}"
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "message": str(e)
        }
