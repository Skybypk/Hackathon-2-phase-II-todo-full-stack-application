from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
try:
    from .routes import tasks
    from .routes import auth
    from .db import engine
    from .models import Task
except ImportError:
    from routes import tasks
    from routes import auth
    from db import engine
    from models import Task
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Todo API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    SQLModel.metadata.create_all(bind=engine)


# Include the routes
app.include_router(tasks.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)