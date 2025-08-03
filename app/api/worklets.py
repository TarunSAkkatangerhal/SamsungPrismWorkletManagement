from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_worklets():
    return [{"id": 1, "title": "AI Chatbot Worklet"}]
