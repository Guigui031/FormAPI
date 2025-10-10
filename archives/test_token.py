"""
Test if token.json is valid and can send emails
"""

import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

def test_token_validity():
    """Test if token.json is valid and can be used"""

    print("🔍 Testing token.json validity...")

    # Check if token.json exists
    if not os.path.exists('token.json'):
        print("❌ token.json not found!")
        return False

    try:
        # Load the token
        with open('token.json', 'r') as f:
            token_data = json.load(f)

        print(f"📄 Token file contents keys: {list(token_data.keys())}")

        # Check if it has required fields
        required_fields = ['token', 'refresh_token', 'token_uri', 'client_id', 'client_secret']
        missing_fields = [field for field in required_fields if field not in token_data]

        if missing_fields:
            print(f"❌ Missing required fields: {missing_fields}")
            return False

        print("✅ Token file has all required fields")

        # Try to load credentials
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        print(f"📊 Token valid: {creds.valid}")
        print(f"📊 Token expired: {creds.expired}")

        # If expired, try to refresh
        if creds.expired and creds.refresh_token:
            print("🔄 Token expired, attempting to refresh...")
            creds.refresh(Request())
            print("✅ Token refreshed successfully!")

            # Save refreshed token
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
            print("💾 Refreshed token saved")

        # Test Gmail API connection
        print("📧 Testing Gmail API connection...")
        service = build("gmail", "v1", credentials=creds)

        # Try to get profile (simple test)
        profile = service.users().getProfile(userId="me").execute()
        print(f"✅ Gmail API connection successful! Email: {profile.get('emailAddress')}")

        return True

    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

def test_send_email():
    """Test actually sending an email"""
    try:
        print("\n📨 Testing email sending...")

        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if creds.expired and creds.refresh_token:
            creds.refresh(Request())

        service = build("gmail", "v1", credentials=creds)

        # Create test email
        email_message = EmailMessage()
        email_message.set_content("This is a test email from the token validation script!")
        email_message["To"] = "guillaumegenois031@gmail.com"
        email_message["From"] = "guillaumegenois031@gmail.com"
        email_message["Subject"] = "Token Test Email"

        # Send email
        encoded_message = base64.urlsafe_b64encode(email_message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        send_message = service.users().messages().send(
            userId="me", body=create_message).execute()

        print(f"✅ Email sent successfully! Message ID: {send_message['id']}")
        return True

    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

if __name__ == "__main__":
    if test_token_validity():
        test_send_email()
    else:
        print("\n❌ Token validation failed. Cannot test email sending.")