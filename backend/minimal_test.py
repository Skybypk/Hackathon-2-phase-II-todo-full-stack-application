import sys
import os
sys.path.insert(0, os.path.abspath('.'))

# Test importing the main components individually
print("Testing individual imports...")

try:
    print("Importing FastAPI...")
    from fastapi import FastAPI
    print("✓ FastAPI imported")
    
    print("Importing CORS middleware...")
    from fastapi.middleware.cors import CORSMiddleware
    print("✓ CORS middleware imported")
    
    print("Importing routes...")
    from routes import tasks, auth
    print("✓ Routes imported")
    
    print("Importing database modules...")
    from db import engine, ensure_tables_exist
    print("✓ Database modules imported")
    
    print("Importing main app...")
    from main import app
    print("✓ Main app imported")
    
    print("Ensuring tables exist...")
    ensure_tables_exist()
    print("✓ Tables ensured")
    
    print("\nAll imports successful! Creating minimal server...")
    
    # Create a minimal server to test
    import uvicorn
    
    print("Starting server on 127.0.0.1:8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", reload=False)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")