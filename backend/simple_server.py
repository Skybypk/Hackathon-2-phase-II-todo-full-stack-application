import sys
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath('.'))

print("Setting up backend server...")

try:
    # Import the app
    from main import app
    print("Successfully imported main app")
    
    # Import uvicorn
    import uvicorn
    print("Successfully imported uvicorn")
    
    # Start the server
    print("Starting server on 0.0.0.0:8000...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        log_level="info",
        reload=False  # Disable reload to prevent issues
    )
    
except Exception as e:
    print(f"Error starting server: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")