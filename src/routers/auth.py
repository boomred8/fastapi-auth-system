from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from sqlalchemy import select

from src.database import SessionDep
from src.models import UserModel
from src.authorization import verify_password, security, get_current_user


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

templates = Jinja2Templates(directory="templates")

@auth_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@auth_router.post("/login")
async def login(
        session: SessionDep,
        form: OAuth2PasswordRequestForm = Depends()
):
    result = await session.execute(
        select(UserModel).where(UserModel.username == form.username)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not verify_password(form.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = security.create_access_token(uid=str(user.id))
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@auth_router.get("/me")
async def me(
        user = Depends(get_current_user)
):
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "is_active": user.is_active
    }