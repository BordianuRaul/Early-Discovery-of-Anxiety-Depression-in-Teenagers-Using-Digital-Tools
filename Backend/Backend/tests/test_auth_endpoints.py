import requests

# Define the base URL for the endpoints
base_url = 'http://127.0.0.1:5000/auth'

# Test data for registration and login
register_data = {
    "username": "testuser",
    "password": "testpassword"
}

login_data = {
    "username": "testuser",
    "password": "testpassword"
}

# Test the registration endpoint
def test_register():
    url = f"{base_url}/register"
    response = requests.post(url, json=register_data)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print("Register Response:", response_json)
    print("Response", response.status_code)
    assert response.status_code == 201

# Test the login endpoint
def test_login():
    url = f"{base_url}/login"
    response = requests.post(url, json=login_data)
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        response_json = {"error": "Invalid JSON response"}
    print("Login Response:", response_json)
    assert response.status_code == 200

# Run the tests
if __name__ == "__main__":
    test_register()
    test_login()