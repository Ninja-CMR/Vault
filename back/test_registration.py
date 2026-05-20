import requests
import json

BASE_URL = "http://localhost:8000"

def test_registration():
    print("Testing User Registration...")
    
    # 1. Test Valid Registration
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "Password123!"
    }
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            print("SUCCESS: User created successfully.")
        else:
            print("FAILURE: User creation failed.")
            
    except Exception as e:
        print(f"Error: {e}")

    # 2. Test Duplicate Email
    print("\nTesting Duplicate Email...")
    response = requests.post(f"{BASE_URL}/auth/register", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

    # 3. Test Invalid Password (too short)
    print("\nTesting Weak Password (too short)...")
    payload_weak = {
        "email": "weak@example.com",
        "password": "short"
    }
    response = requests.post(f"{BASE_URL}/auth/register", json=payload_weak)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_registration()
