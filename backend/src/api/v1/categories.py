from typing import List
from uuid import UUID

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("")
async def get_categories():
    ...


@router.get("/{uuid}")
async def get_category_by_uuid():
    ...


@router.post("/")
async def add_category():
    ...


@router.put("/{uuid}")
async def update_category():
    ...


@router.delete("/{uuid}")
async def remove_category_by_uuid():
    ...
