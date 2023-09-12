from fastapi import APIRouter
from sqlalchemy import text
from starlette.responses import RedirectResponse

from src.api.dependencies import Session

router = APIRouter(tags=["Utils"])


@router.get("/")
async def redirect_to_docs():
    return RedirectResponse("/docs")


@router.get("/ping")
async def ping(session: Session):
    await session.execute(text("SELECT 1"))
    return {"ping": "pong"}
