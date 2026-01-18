"""
Basic API test script to verify the endpoints are working correctly.
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api"

def test_api():
    print("Testing API endpoints...")

    # Test health check
    try:
        response = requests.get(f"{BASE_URL}/../health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        print("Make sure the backend server is running on http://localhost:8000")
        return

    # Test register endpoint
    print("\n--- Testing Registration ---")
    try:
        register_data = {
            "email": f"testuser_{int(datetime.now().timestamp())}@example.com",
            "password": "SecurePassword123!"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"Registration: {response.status_code}")
        if response.status_code == 201:
            print(f"User registered successfully: {response.json()}")
            user_data = response.json()
        else:
            print(f"Registration failed: {response.text}")
            # Try to login if user already exists
            response = requests.post(f"{BASE_URL}/auth/login", data={
                "email": register_data["email"],
                "password": register_data["password"]
            })
            if response.status_code == 200:
                print(f"Login successful: {response.json()}")
                user_data = {"id": response.json()["user"]["id"]}
                auth_token = response.json()["access_token"]
    except Exception as e:
        print(f"Registration test failed: {e}")
        return

    # Test login endpoint
    print("\n--- Testing Login ---")
    try:
        login_data = {
            "email": register_data["email"],
            "password": "SecurePassword123!"
        }
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            print(f"Login successful: {response.json()}")
            auth_token = response.json()["access_token"]
        else:
            print(f"Login failed: {response.text}")
            return
    except Exception as e:
        print(f"Login test failed: {e}")
        return

    # Test get current user
    print("\n--- Testing Get Current User ---")
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Get current user: {response.status_code}")
        if response.status_code == 200:
            print(f"Current user: {response.json()}")
        else:
            print(f"Get current user failed: {response.text}")
    except Exception as e:
        print(f"Get current user test failed: {e}")

    # Test creating a task
    print("\n--- Testing Create Task ---")
    try:
        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }
        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
        print(f"Create task: {response.status_code}")
        if response.status_code == 201:
            print(f"Task created: {response.json()}")
            task_id = response.json()["id"]
        else:
            print(f"Create task failed: {response.text}")
            return
    except Exception as e:
        print(f"Create task test failed: {e}")
        return

    # Test getting all tasks
    print("\n--- Testing Get All Tasks ---")
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{BASE_URL}/tasks", headers=headers)
        print(f"Get all tasks: {response.status_code}")
        if response.status_code == 200:
            print(f"All tasks: {len(response.json())} found")
            if len(response.json()) > 0:
                print(f"First task: {response.json()[0]}")
        else:
            print(f"Get all tasks failed: {response.text}")
    except Exception as e:
        print(f"Get all tasks test failed: {e}")

    # Test getting specific task
    print("\n--- Testing Get Specific Task ---")
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        print(f"Get specific task: {response.status_code}")
        if response.status_code == 200:
            print(f"Specific task: {response.json()}")
        else:
            print(f"Get specific task failed: {response.text}")
    except Exception as e:
        print(f"Get specific task test failed: {e}")

    # Test updating task
    print("\n--- Testing Update Task ---")
    try:
        update_data = {
            "title": "Updated Test Task",
            "description": "This is an updated test task",
            "completed": False
        }
        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=update_data, headers=headers)
        print(f"Update task: {response.status_code}")
        if response.status_code == 200:
            print(f"Task updated: {response.json()}")
        else:
            print(f"Update task failed: {response.text}")
    except Exception as e:
        print(f"Update task test failed: {e}")

    # Test toggling task completion
    print("\n--- Testing Toggle Task Completion ---")
    try:
        toggle_data = {"completed": True}
        headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
        response = requests.patch(f"{BASE_URL}/tasks/{task_id}/complete", json=toggle_data, headers=headers)
        print(f"Toggle task completion: {response.status_code}")
        if response.status_code == 200:
            print(f"Task completion toggled: {response.json()}")
        else:
            print(f"Toggle task completion failed: {response.text}")
    except Exception as e:
        print(f"Toggle task completion test failed: {e}")

    # Test deleting task
    print("\n--- Testing Delete Task ---")
    try:
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}", headers=headers)
        print(f"Delete task: {response.status_code}")
        if response.status_code == 204:
            print("Task deleted successfully")
        else:
            print(f"Delete task failed: {response.text}")
    except Exception as e:
        print(f"Delete task test failed: {e}")

    print("\n--- API Testing Complete ---")

if __name__ == "__main__":
    test_api()