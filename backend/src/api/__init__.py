from fastapi import APIRouter

from backend.src.api.router import router as api_router
from backend.src.api.utils import router as utils_router

router = APIRouter()

router.include_router(api_router)
router.include_router(utils_router)
