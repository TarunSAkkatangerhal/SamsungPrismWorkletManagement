from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
def login():
    return {"message": "User login endpoint"}

@router.post("/register")
def register():
    return {"message": "User register endpoint"}
