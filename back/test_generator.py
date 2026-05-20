import requests
import json
import uuid

BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"gen_test_{uuid.uuid4().hex[:6]}@example.com"
TEST_PASSWORD = "Password123!"

def test_password_generator():
    print(f"Testing Password Generator for user: {TEST_EMAIL}")
    
    # 1. Setup (Login)
    requests.post(f"{BASE_URL}/auth/register", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Test Default Generation
    print("\n2. Testing default generation (16 chars)...")
    resp = requests.post(f"{BASE_URL}/tools/password-generator", json={}, headers=headers)
    print(f"Status: {resp.status_code}")
    assert resp.status_code == 200
    data = resp.json()
    print(f"Generated Password: {data['password']}")
    print(f"Strength: {data['strength']}")
    print(f"Entropy: {data['entropy_score']}")
    assert len(data['password']) == 16

    # 3. Test Custom Generation (Length 32, no symbols)
    print("\n3. Testing custom generation (32 chars, no symbols)...")
    payload = {
        "length": 32,
        "include_symbols": False
    }
    resp = requests.post(f"{BASE_URL}/tools/password-generator", json=payload, headers=headers)
    print(f"Status: {resp.status_code}")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data['password']) == 32
    # Ensure no symbols
    import string
    for char in data['password']:
        assert char not in string.punctuation

    # 4. Test Minimum Length
    print("\n4. Testing minimum length (8 chars)...")
    resp = requests.post(f"{BASE_URL}/tools/password-generator", json={"length": 8}, headers=headers)
    assert len(resp.json()['password']) == 8

    # 5. Authorization Check
    print("\n5. Testing authorization (unauthenticated)...")
    resp = requests.post(f"{BASE_URL}/tools/password-generator", json={})
    print(f"Unauthenticated Status: {resp.status_code}")
    assert resp.status_code == 401

    print("\nALL GENERATOR TESTS PASSED!")

if __name__ == "__main__":
    try:
        test_password_generator()
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
