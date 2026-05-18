from fastapi import APIRouter

router = APIRouter()


@router.post("/analyze")
def analyze_ad(payload: dict):

    return {
        "input": payload,
        "analysis": {
            "score": 75,
            "message": "mock AI response"
        }
    }