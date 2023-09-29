from fastapi import APIRouter

from src.api.v1.categories import router as categories_router
from src.api.v1.expenses import router as expenses_router
from src.api.v1.users import router as users_router

router = APIRouter(prefix="/v1")


registered_routers = [
    users_router,
    categories_router,
    # expenses_router,
]

for rout in registered_routers:
    router.include_router(rout)
