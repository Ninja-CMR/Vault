import requests
import json
import uuid

BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"secret_test_{uuid.uuid4().hex[:6]}@example.com"
TEST_PASSWORD = "Password123!"

def test_secrets_flow():
    print(f"Testing Secrets Flow for user: {TEST_EMAIL}")
    
    # 1. Setup (User + Vault)
    print("\n1. Setting up user and vault...")
    requests.post(f"{BASE_URL}/auth/register", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    login_resp = requests.post(f"{BASE_URL}/auth/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    vault_resp = requests.post(f"{BASE_URL}/vaults", json={"name": "Coffre de tests", "description": "Pour les secrets"}, headers=headers)
    vault_id = vault_resp.json()["id"]

    # 2. Create Secret
    print("\n2. Creating secret...")
    secret_payload = {
        "title": "Ma Clé API Ultra Secrète",
        "type": "API_KEY",
        "value": "sk-1234567890abcdef",
        "description": "Clé pour le service X"
    }
    resp = requests.post(f"{BASE_URL}/vaults/{vault_id}/secrets", json=secret_payload, headers=headers)
    print(f"Create Secret Status: {resp.status_code}")
    assert resp.status_code == 201
    secret_id = resp.json()["id"]
    print(f"Secret ID: {secret_id}")

    # 3. List Secrets (Metadata check)
    print("\n3. Listing secrets (checking metadata)...")
    resp = requests.get(f"{BASE_URL}/vaults/{vault_id}/secrets", headers=headers)
    print(f"List Secrets Status: {resp.status_code}")
    assert resp.status_code == 200
    secrets = resp.json()
    assert len(secrets) == 1
    assert "encrypted_value" not in secrets[0]
    assert secrets[0]["title"] == "Ma Clé API Ultra Secrète"

    # 4. Reveal Secret
    print("\n4. Revealing secret (decryption)...")
    resp = requests.get(f"{BASE_URL}/secrets/{secret_id}/reveal", headers=headers)
    print(f"Reveal Secret Status: {resp.status_code}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["decrypted_value"] == "sk-1234567890abcdef"
    print("Decrypted value matches original!")

    # 5. Authorization Check (Unauthorized user)
    print("\n5. Testing authorization (another user)...")
    OTHER_EMAIL = f"other_{uuid.uuid4().hex[:6]}@example.com"
    requests.post(f"{BASE_URL}/auth/register", json={"email": OTHER_EMAIL, "password": TEST_PASSWORD})
    other_login = requests.post(f"{BASE_URL}/auth/login", json={"email": OTHER_EMAIL, "password": TEST_PASSWORD})
    other_token = other_login.json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    
    # Try to reveal secret of the first user
    resp = requests.get(f"{BASE_URL}/secrets/{secret_id}/reveal", headers=other_headers)
    print(f"Unauthorized Reveal Status: {resp.status_code}")
    assert resp.status_code == 404 # Service uses 404 for not found OR unauthorized

    # 6. Delete Secret
    print("\n6. Deleting secret...")
    resp = requests.delete(f"{BASE_URL}/secrets/{secret_id}", headers=headers)
    print(f"Delete Secret Status: {resp.status_code}")
    assert resp.status_code == 204

    # 7. Verify Deletion
    print("\n7. Verifying deletion...")
    resp = requests.get(f"{BASE_URL}/secrets/{secret_id}", headers=headers)
    print(f"Get Deleted Secret Status: {resp.status_code}")
    assert resp.status_code == 404

    print("\nALL SECRET TESTS PASSED!")

if __name__ == "__main__":
    try:
        test_secrets_flow()
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
