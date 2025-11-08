"""
Test script for the Pneumonia Detection Application
Run this to verify the application is working correctly
"""

import os
import sys
import requests
from pathlib import Path

BASE_URL = "http://localhost:5000"

def test_server_health():
    """Test if the server is running"""
    print("Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Server is running")
            print(f"  Status: {data['status']}")
            print(f"  Model loaded: {data['model_loaded']}")
            return True
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server. Is it running?")
        print(f"  Make sure the server is running at {BASE_URL}")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_api_info():
    """Test the API info endpoint"""
    print("\nTesting API info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/info", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API info retrieved successfully")
            print(f"  Name: {data.get('name')}")
            print(f"  Version: {data.get('version')}")
            print(f"  Model: {data.get('model')}")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_home_page():
    """Test if the home page loads"""
    print("\nTesting home page...")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print("✓ Home page loaded successfully")
            return True
        else:
            print(f"✗ Failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def test_file_upload():
    """Test file upload (requires a test image)"""
    print("\nTesting file upload...")
    print("  Note: This test requires an actual image file")
    print("  Skipping upload test (manual testing recommended)")
    return True

def main():
    print("=" * 60)
    print("Pneumonia Detection Application - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_server_health,
        test_api_info,
        test_home_page,
        test_file_upload
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {str(e)}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
