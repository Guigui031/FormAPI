"""
Test Gmail send functionality WITHOUT accessing profile
(which requires different scopes)
"""

import os
import json
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

def test_send_only():
    """Test ONLY the email sending (not profile access)"""

    print("📧 Testing Gmail SEND functionality only...")

    if not os.path.exists('token.json'):
        print("❌ token.json not found!")
        return False

    try:
        # Load credentials
        SCOPES = ['https://www.googleapis.com/auth/gmail.send']
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        print(f"✅ Token loaded")
        print(f"📊 Token valid: {creds.valid}")
        print(f"📊 Token expired: {creds.expired}")

        # Refresh if needed
        if creds.expired and creds.refresh_token:
            print("🔄 Refreshing expired token...")
            creds.refresh(Request())
            print("✅ Token refreshed")

        # Build Gmail service
        service = build("gmail", "v1", credentials=creds)
        print("✅ Gmail service created")

        # Create test email
        email_message = EmailMessage()
        email_message.set_content("""
This is a test email from the FormAPI token test!

If you received this, the Gmail API sending is working correctly.

Token scopes: gmail.send only
        """)

        email_message["To"] = "guillaumegenois031@gmail.com"
        email_message["From"] = "guillaumegenois031@gmail.com"
        email_message["Subject"] = "🧪 FormAPI Token Send Test"

        # Encode and send
        encoded_message = base64.urlsafe_b64encode(email_message.as_bytes()).decode()
        create_message = {"raw": encoded_message}

        print("📨 Attempting to send email...")

        send_message = service.users().messages().send(
            userId="me",
            body=create_message
        ).execute()

        print(f"✅ SUCCESS! Email sent!")
        print(f"📧 Message ID: {send_message['id']}")
        print("📮 Check your inbox at guillaumegenois031@gmail.com")

        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_api_endpoint():
    """Test the actual Flask API endpoint"""
    import requests

    print("\n🔌 Testing Flask API endpoint...")

    try:
        url = "http://localhost:5000/api/contact"
        data = {
            "name": "Token Test",
            "email": "test@example.com",
            "subject": "API Token Test",
            "message": "Testing if the API can send emails with the current token."
        }

        response = requests.post(url, json=data, timeout=30)

        if response.status_code == 200:
            print("✅ API endpoint SUCCESS!")
            print(f"📄 Response: {response.json()}")
        else:
            print(f"❌ API endpoint FAILED: {response.status_code}")
            print(f"📄 Response: {response.text}")

    except requests.exceptions.ConnectionError:
        print("⚠️  API not running. Start with: python app.py")
    except Exception as e:
        print(f"❌ API test error: {e}")

if __name__ == "__main__":
    if test_send_only():
        print("\n" + "="*50)
        print("🎉 Direct Gmail API sending works!")
        test_api_endpoint()
    else:
        print("\n❌ Gmail API sending failed. Check your token and Google Cloud Console setup.")