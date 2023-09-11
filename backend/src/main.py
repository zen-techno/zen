from fastapi import FastAPI

from backend.src.api import router

app = FastAPI(title="Zen", summary="REST API сервис для управления личными финансами")

app.include_router(router)
