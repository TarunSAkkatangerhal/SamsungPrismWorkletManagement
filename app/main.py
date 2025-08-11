from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, worklets
from app.db import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Samsung PRISM Worklet Management API",
    description="Backend API for managing worklets in Samsung PRISM program",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Samsung PRISM Worklet Management API"}

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(worklets.router, prefix="/worklets", tags=["Worklets"])
