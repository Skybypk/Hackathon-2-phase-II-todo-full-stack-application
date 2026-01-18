from fastapi import FastAPI
from app.api import auth, tasks
from app.database.engine import engine
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from app.models.user import User
from app.models.task import Task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    SQLModel.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Todo API",
    description="A simple todo application API with authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}