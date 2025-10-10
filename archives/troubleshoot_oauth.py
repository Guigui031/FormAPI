"""
Troubleshoot OAuth consent screen issues
"""

import json
import os

def check_oauth_setup():
    """Check OAuth setup issues"""

    print("🔍 OAuth Troubleshooting Guide")
    print("="*50)

    # Check token scopes
    if os.path.exists('token.json'):
        with open('token.json', 'r') as f:
            token_data = json.load(f)

        scopes = token_data.get('scopes', [])
        print(f"📋 Current token scopes: {scopes}")

        if 'https://www.googleapis.com/auth/gmail.send' in scopes:
            print("✅ Gmail send scope is present")
        else:
            print("❌ Gmail send scope is missing!")

    print("\n🔧 TROUBLESHOOTING STEPS:")
    print("1. Go to Google Cloud Console → Your project")
    print("2. APIs & Services → OAuth consent screen")
    print("3. Check your app status:")
    print("   - If 'Testing': Add your email to test users")
    print("   - Better: Click 'PUBLISH APP' to make it public")
    print("4. APIs & Services → Enabled APIs")
    print("   - Verify 'Gmail API' is enabled")
    print("5. Try re-authenticating:")
    print("   - Delete token.json")
    print("   - Visit /auth endpoint again")
    print("   - Google should ask for 'Send email on your behalf'")

    print("\n🚨 COMMON ISSUES:")
    print("- App in 'Testing' mode with wrong test users")
    print("- Gmail API not enabled in the project")
    print("- OAuth consent screen not properly configured")
    print("- Using personal Gmail with strict security settings")

    print("\n💡 QUICK FIX ATTEMPTS:")
    print("1. Publish your app (removes testing restrictions)")
    print("2. Add your Gmail to test users if keeping in testing")
    print("3. Try with a different Google account")
    print("4. Enable 2-factor auth on your Google account")

if __name__ == "__main__":
    check_oauth_setup()