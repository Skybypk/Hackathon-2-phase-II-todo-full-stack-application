import sys
import os
import traceback
from datetime import datetime

# Redirect stdout and stderr to a log file to capture any output
log_file = "server_debug.log"
with open(log_file, "w") as f:
    f.write(f"Debug log started at {datetime.now()}\n")
    f.write(f"Python executable: {sys.executable}\n")
    f.write(f"Current directory: {os.getcwd()}\n")
    f.write(f"Python path: {str(sys.path[:3])}\n\n")

# Now redirect stdout and stderr to the log file
with open(log_file, "a") as f:
    try:
        f.write("Attempting to import main app...\n")
        from main import app
        f.write("Successfully imported main app\n")
        
        f.write("Attempting to import uvicorn...\n")
        import uvicorn
        f.write("Successfully imported uvicorn\n")
        
        f.write(f"Number of routes: {len(app.routes)}\n")
        f.write(f"App type: {type(app)}\n")
        
        f.write("Starting server...\n")
        f.flush()  # Ensure everything is written to the file
        
        # Start the server with logging to the same file
        uvicorn.run(
            app, 
            host="127.0.0.1", 
            port=8000, 
            log_level="debug",
            access_log=True
        )
        
        f.write("Server stopped normally\n")
        
    except Exception as e:
        f.write(f"Error occurred: {e}\n")
        f.write("Full traceback:\n")
        traceback.print_exc(file=f)
        f.write("\nEnd of error traceback\n")
        
f.write(f"Script ended at {datetime.now()}\n")