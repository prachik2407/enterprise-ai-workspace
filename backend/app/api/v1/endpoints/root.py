from fastapi import APIRouter

router = APIRouter()

@router.get("/", tags=["General"])
def root():
    return {
        "message": "Welcome to Enterprise AI Workspace"
    }