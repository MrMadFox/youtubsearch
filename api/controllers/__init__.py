from fastapi import APIRouter
router = APIRouter()

from .health import router as health_router
from .search import router as search_router

router.include_router(router=health_router, prefix="/health")
router.include_router(router=search_router, prefix="/search")