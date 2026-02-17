import sys
import traceback
from app import app
import uvicorn

print('Attempting to start server...')

try:
    # Test importing all required modules first
    from routes import tasks, auth
    print('Successfully imported routes')
    
    from db import engine, ensure_tables_exist
    print('Successfully imported db modules')
    
    # Run the startup function
    ensure_tables_exist()
    print('Database tables ensured')
    
    print('Starting Uvicorn server on 0.0.0.0:8000...')
    uvicorn.run(app, host='0.0.0.0', port=8000, log_level='info')
    
except Exception as e:
    print(f'Error: {e}')
    print('Full traceback:')
    traceback.print_exc()
    input("Press Enter to continue...")