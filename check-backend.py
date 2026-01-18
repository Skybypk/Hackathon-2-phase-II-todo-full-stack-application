import subprocess
import sys
import time
import requests

def check_backend_status():
    """Check if the backend server is running on localhost:8000"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend server is running and accessible!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server. Is it running on http://localhost:8000?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout while trying to connect to backend server.")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {str(e)}")
        return False

def main():
    print("Checking backend server status...")
    print("Looking for backend at: http://localhost:8000/")

    if check_backend_status():
        print("\n✅ Backend is accessible!")
    else:
        print("\n❌ Backend is not accessible. Please start the backend server:")
        print("   cd E:\\h-2\\backend")
        print("   python main.py")

        # Check if we can see any Python processes running
        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True, shell=True)
            if 'python.exe' in result.stdout.lower():
                print("\n💡 Python processes are running. Check if the backend is one of them.")
            else:
                print("\n💡 No Python processes detected.")
        except:
            print("\n💡 Could not check running processes.")

if __name__ == "__main__":
    main()