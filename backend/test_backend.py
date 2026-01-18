"""
Test script to verify the backend structure and imports work correctly
"""

def test_imports():
    """Test that all modules can be imported without errors"""
    try:
        from main import app
        print("✓ main.py imports successfully")

        from db import engine, get_session
        print("✓ db.py imports successfully")

        from models import Task
        print("✓ models.py imports successfully")

        from auth import get_current_user, verify_token
        print("✓ auth.py imports successfully")

        from dependencies import CurrentUser
        print("✓ dependencies.py imports successfully")

        from routes.tasks import router
        print("✓ routes/tasks.py imports successfully")

        from schemas.task import TaskCreate, TaskUpdate, TaskComplete, Task
        print("✓ schemas/task.py imports successfully")

        print("\nAll modules imported successfully!")
        print("Backend structure is correct.")

    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

    return True

if __name__ == "__main__":
    test_imports()