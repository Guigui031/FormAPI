"""
Run this once to set up Gmail API authentication locally.
This will open a browser window for you to authenticate with Google.
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Gmail API scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def setup_gmail_auth():
    """Set up Gmail API authentication for local development"""
    creds = None

    # Check if token.json already exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json not found!")
                print("Download it from Google Cloud Console and place it in this directory")
                return False

            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()

        # Save credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    print("✅ Gmail API authentication successful!")
    print("You can now run the Flask app and send real emails")
    return True

if __name__ == '__main__':
    setup_gmail_auth()