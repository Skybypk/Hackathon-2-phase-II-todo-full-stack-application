import requests
import time

# Wait a moment to ensure the server is fully ready
time.sleep(2)

# Register a default user
register_data = {
    "email": "admin@example.com",
    "password": "AdminPass12345678!"  # Contains at least 8 digits (1,2,3,4,5,6,7,8)
}

try:
    register_response = requests.post('http://127.0.0.1:8000/api/auth/register', json=register_data, timeout=10)
    
    if register_response.status_code in [200, 201]:
        print('Default user created successfully!')
        print(f'Email: admin@example.com')
        print(f'Password: AdminPass12345678!')
        print('You can now use these credentials to log in.')
    elif register_response.status_code == 409:  # Conflict - user already exists
        print('Default user already exists.')
    else:
        print(f'Failed to create user. Status: {register_response.status_code}, Response: {register_response.text}')
except requests.exceptions.RequestException as e:
    print(f'Error connecting to backend server: {e}')