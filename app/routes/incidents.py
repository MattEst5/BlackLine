from fastapi import APIRouter

router = APIRouter()

@router.get("/incidents")
def get_incidents():
    return{"message": "Here are your incidents."}