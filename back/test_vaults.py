import requests
import json
import uuid

BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"vault_test_{uuid.uuid4().hex[:6]}@example.com"
TEST_PASSWORD = "Password123!"

def test_vaults_flow():
    print(f"Testing Vaults Flow for user: {TEST_EMAIL}")
    
    # 1. Register User
    print("\n1. Registering user...")
    register_payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    resp = requests.post(f"{BASE_URL}/auth/register", json=register_payload)
    print(f"Register Status: {resp.status_code}")
    assert resp.status_code == 201

    # 2. Login
    print("\n2. Logging in...")
    login_payload = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    resp = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
    print(f"Login Status: {resp.status_code}")
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Create Vault
    print("\n3. Creating vault...")
    vault_payload = {
        "name": "Mon Coffre Secret",
        "description": "Contient mes mots de passe importants"
    }
    resp = requests.post(f"{BASE_URL}/vaults", json=vault_payload, headers=headers)
    print(f"Create Vault Status: {resp.status_code}")
    assert resp.status_code == 201
    vault_id = resp.json()["id"]
    print(f"Vault ID: {vault_id}")

    # 4. Create Duplicate Vault (should fail)
    print("\n4. Creating duplicate vault (should fail)...")
    resp = requests.post(f"{BASE_URL}/vaults", json=vault_payload, headers=headers)
    print(f"Duplicate Vault Status: {resp.status_code}")
    assert resp.status_code == 400
    print(f"Error detail: {resp.json()['detail']}")

    # 5. List Vaults
    print("\n5. Listing vaults...")
    resp = requests.get(f"{BASE_URL}/vaults", headers=headers)
    print(f"List Vaults Status: {resp.status_code}")
    assert resp.status_code == 200
    vaults = resp.json()
    assert len(vaults) == 1
    assert vaults[0]["name"] == "Mon Coffre Secret"

    # 6. Get Specific Vault
    print("\n6. Getting specific vault...")
    resp = requests.get(f"{BASE_URL}/vaults/{vault_id}", headers=headers)
    print(f"Get Vault Status: {resp.status_code}")
    assert resp.status_code == 200
    assert resp.json()["id"] == vault_id

    # 7. Delete Vault
    print("\n7. Deleting vault...")
    resp = requests.delete(f"{BASE_URL}/vaults/{vault_id}", headers=headers)
    print(f"Delete Vault Status: {resp.status_code}")
    assert resp.status_code == 204

    # 8. Verify Deletion
    print("\n8. Verifying deletion...")
    resp = requests.get(f"{BASE_URL}/vaults/{vault_id}", headers=headers)
    print(f"Get Deleted Vault Status: {resp.status_code}")
    assert resp.status_code == 404

    print("\nALL VAULT TESTS PASSED!")

if __name__ == "__main__":
    try:
        test_vaults_flow()
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
