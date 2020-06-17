from decouple import config
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GoogleDriveApi:
    SCOPES = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive.metadata']
    CREDENTIALS_FILE = config('CREDENTIALS_FILE', cast=str, default='credentials.json')
    TOKEN_FILE = config('TOKEN_FILE', cast=str, default='token.pickle')

    def __init__(self):
        credentials = self.get_credentials()
        self.service = self.build_service(credentials)

    def get_credentials(self):
        creds = None

        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.CREDENTIALS_FILE, self.SCOPES)
                creds = flow.run_local_server(port=8080)
            # Save the credentials for the next run
            with open(self.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def build_service(self, credentials):
        if not credentials:
            raise Exception('Wrong credentials')

        return build('drive', 'v3', credentials=credentials)

    def upload_file(self, filename, filepath):
        file_metadata = {
            'name': filename,
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        media = MediaFileUpload(filepath, mimetype='application/vnd.google-apps.spreadsheet', resumable=True)
        file = self.service.files().create(
            body=file_metadata, media_body=media, fields='id'
        ).execute()

        return file.get('id')

    def list_files(self):
        # Call the Drive v3 API
        results = self.service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get('files', [])

        return [(item['name'], item['id']) for item in items]


def main():
    api = GoogleDriveApi()

    list_files = api.list_files()
    print(list_files)
    FILENAME = config('FILENAME', cast=str)
    FILEPATH = config('FILEPATH', cast=str)
    uploaded_file_id = api.upload_file(FILENAME, FILEPATH)
    print(uploaded_file_id)
    list_files = api.list_files()
    print(list_files)


if __name__ == '__main__':
    main()
