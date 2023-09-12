from fastapi import APIRouter

from src.api.v1 import router as v1_router

router = APIRouter(prefix="/api")

registered_routers = [
    v1_router,
]


for rout in registered_routers:
    router.include_router(rout)
