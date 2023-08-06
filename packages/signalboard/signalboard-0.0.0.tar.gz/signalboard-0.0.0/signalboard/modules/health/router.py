from fastapi import APIRouter

from signalboard.modules.health.model import Health

health_router = APIRouter(
    prefix="/health",  # /api/health
    tags=["Health"]
)


@health_router.get("/", response_model=Health)
async def health():
    return Health(status='healthy')
