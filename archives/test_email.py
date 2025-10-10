"""
Quick test script to send a test email via the API
"""

import requests
import json

def test_form_api():
    """Test the form API with sample data"""
    url = "http://localhost:5000/api/contact"

    # Test data
    test_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "subject": "API Test Email",
        "message": "This is a test message from the FormAPI. If you receive this, the API is working correctly!"
    }

    try:
        print("🧪 Testing FormAPI...")
        print(f"Sending POST to: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")

        response = requests.post(url, json=test_data)

        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📄 Response Body: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("\n✅ SUCCESS! Check your email inbox.")
        else:
            print(f"\n❌ FAILED! Status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to the API.")
        print("Make sure the Flask app is running with: python app.py")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_form_api()