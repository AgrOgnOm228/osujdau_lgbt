from fastapi import APIRouter
from fastapi.responses import HTMLResponse

import src.service as service

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def get_home_page() -> HTMLResponse:
    return await service.get_home_page()


@router.get("/leaders", response_class=HTMLResponse)
async def get_leaders_page(page: int = 1, size: int = 10) -> HTMLResponse:
    return await service.get_leaders_page(page, size)
