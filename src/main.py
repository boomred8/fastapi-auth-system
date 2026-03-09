import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles

from routers.auth import auth_router
from routers.admin_panel import admin_router
from src.authorization import security

app = FastAPI()
security.handle_errors(app)
app.mount("/static", StaticFiles(directory="static"), name="static")

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(router=auth_router)
api_router.include_router(router=admin_router)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)