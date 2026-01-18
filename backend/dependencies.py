from fastapi import Depends
try:
    from .auth import get_current_user
except ImportError:
    from auth import get_current_user

# Dependency to get the current user from JWT token
def get_current_user_dependency():
    return Depends(get_current_user)

# Or define as a variable (this is the correct way)
CurrentUser = Depends(get_current_user)