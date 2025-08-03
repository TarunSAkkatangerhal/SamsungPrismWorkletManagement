# backend/app/main.py
from fastapi import FastAPI
from app.api import worklets, auth  # (you’ll create these files)

app = FastAPI(
    title="Samsung PRISM Worklet Management System",
    version="1.0.0",
)

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(worklets.router, prefix="/worklets", tags=["Worklets"])

@app.get("/")
def read_root():
    return {"msg": "Welcome to PRISM Worklet API"}
