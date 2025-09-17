from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import base64
import os
from email.message import EmailMessage
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from setup_auth import setup_gmail_auth

app = Flask(__name__)
CORS(app)
app.secret_key = 'your-secret-key-change-this-in-production'

def get_gmail_credentials():
    """Get Gmail API credentials using service account or default credentials"""
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    try:
        # Try to use default credentials (service account or gcloud auth)
        creds, _ = google.auth.default(scopes=SCOPES)
        return creds
    except Exception as e:
        raise Exception(f"No valid credentials found. Error: {e}")

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

@app.route('/debug-redirect', methods=['GET'])
def debug_redirect():
    """Debug endpoint to check redirect URI"""
    redirect_uri = request.url_root + 'auth/callback'
    return jsonify({
        'url_root': request.url_root,
        'redirect_uri': redirect_uri,
        'host': request.host,
        'scheme': request.scheme
    }), 200

@app.route('/auth', methods=['GET'])
def auth():
    """Start OAuth2 authentication flow"""
    from google_auth_oauthlib.flow import Flow
    import secrets

    # Allow insecure transport for development (in production, use HTTPS properly)
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    try:
        # Create flow instance to manage the OAuth2 authorization grant
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/gmail.send'])

        # Set the redirect URI (force HTTPS for production)
        if request.host.startswith('form.guillaume.genois.ca'):
            redirect_uri = 'https://form.guillaume.genois.ca/auth/callback'
        else:
            redirect_uri = request.url_root + 'auth/callback'

        print(f"DEBUG: Using redirect_uri: {redirect_uri}")
        flow.redirect_uri = redirect_uri

        # Generate authorization URL
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')

        # Store state in session for security
        from flask import session
        session['state'] = state

        # Redirect to Google's OAuth2 server
        from flask import redirect
        return redirect(authorization_url)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/auth/callback')
def auth_callback():
    """Handle OAuth2 callback"""
    from google_auth_oauthlib.flow import Flow
    from flask import session

    # Allow insecure transport for development
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    try:
        # Create flow instance
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=['https://www.googleapis.com/auth/gmail.send'],
            state=session['state'])

        # Set the redirect URI (force HTTPS for production)
        if request.host.startswith('form.guillaume.genois.ca'):
            redirect_uri = 'https://form.guillaume.genois.ca/auth/callback'
        else:
            redirect_uri = request.url_root + 'auth/callback'

        flow.redirect_uri = redirect_uri

        # Use authorization response to fetch token
        flow.fetch_token(authorization_response=request.url)

        # Store credentials
        credentials = flow.credentials

        # Save to token.json
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

        return jsonify({
            'status': 'success',
            'message': 'Authentication successful! You can now use the API.'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)