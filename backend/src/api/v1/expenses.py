from fastapi import APIRouter

router = APIRouter(prefix="/expenses", tags=["Expenses"])


@router.get("")
async def get_expenses():
    ...


@router.get("/{uuid}")
async def get_expense_by_uuid():
    ...


@router.post("/")
async def add_expense():
    ...


@router.put("/{uuid}")
async def update_expense():
    ...


@router.delete("/{uuid}")
async def remove_expense_by_uuid():
    ...
