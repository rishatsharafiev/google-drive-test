import os
from decouple import config
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.settings.update({
    'client_config_backend': 'file',
    'client_config_file': 'credentials.json',
    'save_credentials': False,
    'oauth_scope': ['https://www.googleapis.com/auth/drive']
})

gauth.LoadCredentialsFile('credentials_refresh.json')
if gauth.credentials is None:
    # gauth.GetFlow()
    # gauth.flow.params.update({'access_type': 'offline'})
    # gauth.flow.params.update({'approval_prompt': 'force'})

    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
gauth.SaveCredentialsFile('credentials_refresh.json')


drive = GoogleDrive(gauth)


FILENAME = config('FILENAME')  # если передавать русские названия, то не работает, попробуйте передать название файла напрямую в SetContentFile без decouple
FILEPATH = config('FILEPATH')  # если передавать русские названия, то не работает, попробуйте передать название файла напрямую в SetContentFile без decouple

test_file = drive.CreateFile({'title': FILENAME})
test_file.SetContentFile(FILEPATH)
test_file.Upload({'convert': True})  # <--- убрать конвертацию, чтобы грузить таблицы с графиками
test_file.InsertPermission({
    'type':  'anyone',
    'value': 'anyone',
    'role':  'reader',
    'additionalRoles': ['commenter'],
    'withLink': True,
})
