import requests
import time
import subprocess
import signal
import os

# Start the backend server
print("Starting backend server...")
backend_process = subprocess.Popen(['python', 'main.py'], cwd='D:/Quarter-4/Projects/Q4-Hackathon-02/h-2/backend', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait a bit for the server to start
time.sleep(5)

try:
    # Test if the server is running
    response = requests.get('http://localhost:8000/health', timeout=10)
    if response.status_code == 200:
        print("Backend server is running!")

        # Register a default user
        register_data = {
            "email": "admin@example.com",
            "password": "AdminPass12345678!"  # Contains at least 8 digits (1,2,3,4,5,6,7,8)
        }

        register_response = requests.post('http://localhost:8000/api/auth/register', json=register_data)

        if register_response.status_code in [200, 201]:
            print("Default user created successfully!")
            print(f"Email: admin@example.com")
            print(f"Password: AdminPass123!")
            print("You can now use these credentials to log in.")
        elif register_response.status_code == 409:  # Conflict - user already exists
            print("Default user already exists.")
        else:
            print(f"Failed to create user. Status: {register_response.status_code}, Response: {register_response.text}")
    else:
        print(f"Backend server not responding. Status: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"Error connecting to backend server: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    # Stop the backend server
    print("Stopping backend server...")
    backend_process.terminate()
    try:
        backend_process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        backend_process.kill()

    print("Backend server stopped.")