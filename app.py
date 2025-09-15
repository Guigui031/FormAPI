from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
from email.message import EmailMessage
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__)
CORS(app)

def get_gmail_credentials():
    """Get Gmail API credentials for local development or production"""
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    creds = None

    # For local development, try to use token.json
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no local token, try default credentials (production)
    if not creds or not creds.valid:
        try:
            creds, _ = google.auth.default(scopes=SCOPES)
        except Exception:
            # If default fails and we have local token, try to refresh it
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
            else:
                raise Exception("No valid credentials found. Run setup_auth.py first for local testing.")

    return creds

def send_form_email(name, email, subject, message):
    """Send an email with form data using Gmail API"""
    try:
        creds = get_gmail_credentials()
        service = build("gmail", "v1", credentials=creds)

        email_message = EmailMessage()

        # Create email content
        email_content = f"""
New form submission received:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This email was sent automatically from your form API.
        """

        email_message.set_content(email_content)
        email_message["To"] = "guillaumegenois031@gmail.com"
        email_message["From"] = "guillaumegenois031@gmail.com"
        email_message["Subject"] = f"Form Submission: {subject}"

        # Add reply-to header with the sender's email
        email_message["Reply-To"] = email

        # Encode message
        encoded_message = base64.urlsafe_b64encode(email_message.as_bytes()).decode()

        create_message = {"raw": encoded_message}

        send_message = (
            service.users()
            .messages()
            .send(userId="me", body=create_message)
            .execute()
        )

        return send_message["id"]

    except HttpError as error:
        raise Exception(f"Gmail API error: {error}")
    except Exception as error:
        raise Exception(f"Error sending email: {error}")

@app.route('/api/contact', methods=['POST'])
def contact_form():
    """Handle contact form submissions"""
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        for field in required_fields:
            if not data or field not in data or not data[field].strip():
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        name = data['name'].strip()
        email = data['email'].strip()
        subject = data['subject'].strip()
        message = data['message'].strip()

        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({
                'success': False,
                'error': 'Invalid email format'
            }), 400

        # Send email
        message_id = send_form_email(name, email, subject, message)

        return jsonify({
            'success': True,
            'message': 'Form submitted successfully',
            'message_id': message_id
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)