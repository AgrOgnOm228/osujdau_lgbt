import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter

from src.config import settings
from src.routers import router as lid_router
from src.temp import router as tmp_router

app = FastAPI(docs_url=f'{settings.BASE_ROUTE_PATH}/docs')

router = APIRouter(prefix=settings.BASE_ROUTE_PATH)

router.include_router(lid_router, prefix='/lider', tags=['lider'])
app.include_router(tmp_router, tags=['tmp'])

app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(
        app='src.main:app',
        host="127.0.0.1",
        port=8000,
        reload=True
    )
