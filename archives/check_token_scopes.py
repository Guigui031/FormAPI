"""
Check what scopes are in the current token.json
"""

import json
import os

def check_token_scopes():
    """Check what scopes are in the current token"""

    if not os.path.exists('token.json'):
        print("❌ token.json not found!")
        return

    try:
        with open('token.json', 'r') as f:
            token_data = json.load(f)

        print("🔍 Token contents:")
        for key, value in token_data.items():
            if key == 'scopes':
                print(f"  📋 {key}: {value}")
            elif key in ['token', 'refresh_token']:
                print(f"  🔑 {key}: {value[:20]}...")
            else:
                print(f"  📄 {key}: {value}")

        # Check if Gmail send scope is present
        scopes = token_data.get('scopes', [])
        gmail_send_scope = 'https://www.googleapis.com/auth/gmail.send'

        if gmail_send_scope in scopes:
            print(f"✅ Gmail send scope found: {gmail_send_scope}")
        else:
            print(f"❌ Gmail send scope MISSING: {gmail_send_scope}")
            print(f"   Current scopes: {scopes}")
            print("   You need to re-authenticate with the correct scope!")

    except Exception as e:
        print(f"❌ Error reading token: {e}")

if __name__ == "__main__":
    check_token_scopes()