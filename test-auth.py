from google.oauth2 import service_account

# Créez un fichier de clés de service depuis Google Console
credentials = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/gmail.readonly']
)

print(credentials)