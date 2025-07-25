#!/usr/bin/env python3
"""
Simple test script to verify the Flask app works locally
"""
import requests
import json
import time

def test_app():
    base_url = "http://localhost:8080"
    
    print("Testing CSMHelperBot endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✅ Root endpoint: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test POST endpoint
    try:
        test_data = {
            "message": {
                "text": "csm test_account"
            }
        }
        response = requests.post(f"{base_url}/", json=test_data)
        print(f"✅ POST endpoint: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ POST endpoint failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Make sure the Flask app is running on localhost:8080")
    print("Run: python app.py")
    print()
    
    # Wait a moment for the app to start
    time.sleep(2)
    
    if test_app():
        print("\n🎉 All tests passed! App is ready for deployment.")
    else:
        print("\n❌ Some tests failed. Check the app configuration.") 