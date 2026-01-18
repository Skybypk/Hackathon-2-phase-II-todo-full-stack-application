import subprocess
import sys
import time
import requests
from urllib.parse import urlparse

def check_backend_status():
    """Check if the backend server is running on localhost:8000"""
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            print("✅ Backend server is running and accessible!")
            try:
                json_response = response.json()
                if "message" in json_response:
                    print(f"   Response: {json_response['message']}")
            except:
                pass
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

def check_frontend_status():
    """Check if the frontend server is running on localhost:3000"""
    try:
        response = requests.get("http://localhost:3000/", timeout=10)
        if response.status_code == 200:
            print("✅ Frontend server is running and accessible!")
            return True
        elif response.status_code == 404:
            # Even if it's a 404, it means the server is running
            print("✅ Frontend server is running (received 404, which means server is accessible)")
            return True
        else:
            print(f"❌ Frontend server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to frontend server. Is it running on http://localhost:3000?")
        return False
    except requests.exceptions.Timeout:
        print("❌ Timeout while trying to connect to frontend server.")
        return False
    except Exception as e:
        print(f"❌ Error checking frontend: {str(e)}")
        return False

def check_port_availability(port):
    """Check if a specific port is available"""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0

def diagnose_issues():
    """Diagnose common issues"""
    print("\n🔍 Diagnosing common issues...")

    # Check if ports are available
    backend_port_free = check_port_availability(8000)
    frontend_port_free = check_port_availability(3000)

    if not backend_port_free:
        print("⚠️  Port 8000 (backend) might be in use by another process")
        try:
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if ':8000' in line:
                    print(f"   Process using port 8000: {line.strip()}")
        except:
            pass

    if not frontend_port_free:
        print("⚠️  Port 3000 (frontend) might be in use by another process")
        try:
            result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if ':3000' in line:
                    print(f"   Process using port 3000: {line.strip()}")
        except:
            pass

def main():
    print("🔍 Service Connectivity Checker")
    print("="*50)

    print("Checking backend server status...")
    print("Looking for backend at: http://localhost:8000/")
    backend_ok = check_backend_status()

    print("\nChecking frontend server status...")
    print("Looking for frontend at: http://localhost:3000/")
    frontend_ok = check_frontend_status()

    print("\n📋 Status Summary:")
    print(f"   Backend (8000): {'✅ Running' if backend_ok else '❌ Not accessible'}")
    print(f"   Frontend (3000): {'✅ Running' if frontend_ok else '❌ Not accessible'}")

    if not backend_ok:
        print("\n💡 To start the backend server:")
        print("   1. Open a command prompt")
        print("   2. Run: start-backend.bat")
        print("   OR manually:")
        print("      cd E:\\h-2\\backend")
        print("      python main.py")

    if not frontend_ok:
        print("\n💡 To start the frontend server:")
        print("   1. Open a new command prompt")
        print("   2. Run:")
        print("      cd E:\\h-2\\frontend")
        print("      npm run dev")

    if not backend_ok or not frontend_ok:
        diagnose_issues()

    print(f"\n📖 For detailed instructions, see: STARTUP_GUIDE.md")

    return backend_ok and frontend_ok

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 All services are running properly!")
    else:
        print("\n⚠️  Some services are not accessible. Please follow the instructions above.")
    sys.exit(0 if success else 1)