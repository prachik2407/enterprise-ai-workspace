from fastapi import APIRouter

from app.api.v1.endpoints.root import router as root_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.documents import router as documents_router


router = APIRouter(prefix="/api/v1")

router.include_router(root_router)
router.include_router(health_router)
router.include_router(auth_router)
router.include_router(documents_router)