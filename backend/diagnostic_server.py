import sys
import traceback
import logging

# Set up logging to capture all output
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

print('Starting backend server diagnostics...')

try:
    print('Importing FastAPI...')
    from fastapi import FastAPI
    print('FastAPI imported successfully')
    
    print('Importing routes...')
    from routes import tasks, auth
    print('Routes imported successfully')
    
    print('Importing db modules...')
    from db import engine, ensure_tables_exist
    print('DB modules imported successfully')
    
    print('Importing main app...')
    from main import app
    print('Main app imported successfully')
    
    print('Ensuring database tables exist...')
    ensure_tables_exist()
    print('Database tables ensured')
    
    print('Importing uvicorn...')
    import uvicorn
    print('Uvicorn imported successfully')
    
    print('All imports successful. Ready to start server.')
    
    # Start the server
    print('Starting server on 0.0.0.0:8000...')
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='debug')
    
except ImportError as e:
    print(f'Import error: {e}')
    traceback.print_exc()
except Exception as e:
    print(f'General error: {e}')
    traceback.print_exc()
    
print('Server script completed.')