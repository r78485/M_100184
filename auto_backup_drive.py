import os
import shutil
import zipfile
import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

# --- Configuration ---
# Path to the service account JSON key file (You must create this in Google Cloud Console)
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Google Drive folder ID where backups will be stored. (Get this from the folder URL)
# Example: https://drive.google.com/drive/folders/1aBcDeFgHiJkLmNoPqRsTuVwXyZ?usp=sharing
# The ID is '1aBcDeFgHiJkLmNoPqRsTuVwXyZ'
# If left empty, it will upload to the root directory of the Service Account.
DRIVE_FOLDER_ID = ''

# Files/Directories to backup
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(PROJECT_ROOT, 'db.sqlite3')
MEDIA_FOLDER = os.path.join(PROJECT_ROOT, 'media')

# Scopes for Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def create_backup_zip():
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    zip_filename = f'system_backup_{timestamp}.zip'
    zip_path = os.path.join(PROJECT_ROOT, zip_filename)
    
    # Exclude these directories from the backup to save space & prevent hanging
    EXCLUDE_DIRS = {
        'venv', '.venv', 'env', '__pycache__', '.git', '.vscode', '.idea',
        'android', 'android_app', 'flutter_app', 'EduManage_Offline_Software',
        'node_modules', '.gemini', 'brain', 'tmp', 'dist', 'build', 'gradle'
    }
    
    print(f"Creating full system backup archive: {zip_filename}...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
        for foldername, subfolders, filenames in os.walk(PROJECT_ROOT):
            # Modify subfolders in-place to avoid walking into excluded directories
            subfolders[:] = [d for d in subfolders if d not in EXCLUDE_DIRS and not d.startswith('.')]
            
            for filename in filenames:
                # Do not backup any zip file or temporary journal/lock files
                if filename.endswith('.zip') or filename.endswith('-journal') or filename.endswith('-wal') or filename == zip_filename:
                    continue
                
                file_path = os.path.join(foldername, filename)
                try:
                    arcname = os.path.relpath(file_path, PROJECT_ROOT)
                    backup_zip.write(file_path, arcname=arcname)
                except Exception as err:
                    print(f"Skipping file {file_path}: {err}")
                    
    print("Backup archive created successfully.")
    return zip_path

def authenticate_gdrive():
    print("Authenticating with Google Drive API...")
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"Credentials file '{SERVICE_ACCOUNT_FILE}' not found. Please create a Service Account in Google Cloud and save the JSON key here.")
        
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def upload_to_drive(service, file_path):
    print(f"Uploading {os.path.basename(file_path)} to Google Drive...")
    file_metadata = {'name': os.path.basename(file_path)}
    if DRIVE_FOLDER_ID:
        file_metadata['parents'] = [DRIVE_FOLDER_ID]
        
    media = MediaFileUpload(file_path, mimetype='application/zip', resumable=True)
    
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    
    print(f"Upload complete! Google Drive File ID: {file.get('id')}")

def main():
    zip_path = None
    try:
        zip_path = create_backup_zip()
        service = authenticate_gdrive()
        upload_to_drive(service, zip_path)
    except Exception as e:
        print(f"Error during backup process: {str(e)}")
    finally:
        # Clean up the local zip file after upload
        if zip_path and os.path.exists(zip_path):
            os.remove(zip_path)
            print("Cleaned up local backup file.")

if __name__ == '__main__':
    main()
