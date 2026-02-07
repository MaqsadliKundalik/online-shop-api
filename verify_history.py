
import sys
import os
import json

# Add current directory to sys.path
sys.path.append(os.getcwd())

try:
    from fastapi.testclient import TestClient
    from app.main import app
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)

def verify_history_endpoint():
    print("Initializing TestClient...")
    client = TestClient(app)

    print("\n--- Testing GET /api/v1/orders/history ---")
    # Test with a dummy customer_id
    customer_id = 999999
    response = client.get(f"/api/v1/orders/history?customer_id={customer_id}")
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("Response JSON (should be empty list for dummy ID):")
        print(response.json())
        print("SUCCESS: Endpoint is reachable and working.")
    else:
        print("FAILURE: Endpoint returned error.")
        print(response.text)

    print("\n--- Generating JSON Docs (openapi.json) ---")
    response_docs = client.get("/openapi.json")
    if response_docs.status_code == 200:
        with open("openapi_docs.json", "w", encoding="utf-8") as f:
            json.dump(response_docs.json(), f, indent=2)
        print("SUCCESS: Saved OpenAPI docs to 'openapi_docs.json'.")
    else:
        print("FAILURE: Could not fetch openapi.json")

if __name__ == "__main__":
    verify_history_endpoint()
