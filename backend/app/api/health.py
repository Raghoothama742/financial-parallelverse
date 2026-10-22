from fastapi import APIRouter
from ..schemas import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("", response_model=HealthResponse)
def get_health():
    return HealthResponse(status="healthy", version="1.0.0")
