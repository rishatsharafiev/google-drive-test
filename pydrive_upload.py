from decouple import config
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.settings.update({
    'client_config_file': 'credentials.json',
})
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


FILENAME = config('FILENAME', cast=str)
FILEPATH = config('FILEPATH', cast=str)

test_file = drive.CreateFile({'title': FILENAME})
test_file.SetContentFile(FILEPATH)
test_file.InsertPermission({
    'type':  'anyone',
    'value': 'anyone',
    'role':  'reader',
    'additionalRoles': ['commenter'],
    'withLink': True,
})
test_file.Upload({'convert': True})
