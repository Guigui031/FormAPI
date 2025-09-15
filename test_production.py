"""
Test script for production API deployment
"""

import requests
import json

def test_production_api():
    """Test the production form API"""
    url = "https://form.guillaume.genois.ca/api/contact"

    # Test data
    test_data = {
        "name": "Production Test",
        "email": "test@example.com",
        "subject": "Production API Test",
        "message": "This is a test of the production FormAPI deployment!"
    }

    try:
        print("🚀 Testing Production FormAPI...")
        print(f"URL: {url}")
        print(f"Data: {json.dumps(test_data, indent=2)}")

        response = requests.post(url, json=test_data, timeout=30)

        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📄 Response Body: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("\n✅ SUCCESS! Production API is working!")
            print("Check your email inbox for the test message.")
        else:
            print(f"\n❌ FAILED! Status code: {response.status_code}")

    except requests.exceptions.SSLError:
        print("❌ SSL Error - Certificate might not be set up correctly")
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error - Server might be down or DNS not configured")
    except requests.exceptions.Timeout:
        print("❌ Timeout - Server is taking too long to respond")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_health_check():
    """Test the health check endpoint"""
    try:
        response = requests.get("https://form.guillaume.genois.ca/health", timeout=10)
        print(f"Health Check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health Check Failed: {e}")

if __name__ == "__main__":
    test_health_check()
    test_production_api()