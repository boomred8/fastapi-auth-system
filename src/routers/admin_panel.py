from urllib.request import Request

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select

from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.models import UserModel
from src.schemas import UserAddByAdminSchema
from src.database import SessionDep
from src.authorization import get_current_admin
from src.authorization import hash_password

admin_router = APIRouter(prefix="/admin-panel",
                         tags=["admin panel"])


templates = Jinja2Templates(directory="templates")

@admin_router.get(
    "/page",
    response_class=HTMLResponse
)
async def admin_panel_page(request: Request):
    return templates.TemplateResponse(
        "admin-panel.html",
        {
            "request": request,
        }
    )


@admin_router.post("/users",
                   description="Add new user")
async def create_user(
        session: SessionDep,
        data: UserAddByAdminSchema,
        admin: UserModel = Depends(get_current_admin),
):

   result = await session.execute(
       select(UserModel).where(UserModel.username == data.username)
   )
   existing_user = result.scalars().first()

   if existing_user:
       raise HTTPException(status_code=409, detail="User already exists")

   new_user = UserModel(
       username=data.username,
       password=hash_password(data.password),
       role=data.role
   )

   session.add(new_user)
   await session.commit()
   await session.refresh(new_user)

   return {
       "id": new_user.id,
       "username": new_user.username,
       "role": new_user.role,
       "is_active": new_user.is_active
   }