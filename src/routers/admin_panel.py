from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select

from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.models import UserModel
from src.schemas import UserAddByAdminSchema, UserUpdateSchema, UserReadSchema
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

@admin_router.get("/users",
                  response_model=List[UserReadSchema]) #для таблицы чтобы юзер знал какие есть
async def all_users(
        session: SessionDep,
        admin: UserModel = Depends(get_current_admin),
):
    result = await session.execute(select(UserModel))
    users = result.scalars().all()

    return users




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

@admin_router.patch("/users/{user_id}",
                    response_model=UserReadSchema)
async def update_user(
        session: SessionDep,
        new_data: UserUpdateSchema,
        user_id: int,
        admin: UserModel = Depends(get_current_admin)
):
    result = await session.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    existing_user = result.scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if existing_user.role == "admin":
        raise HTTPException(status_code=409, detail="Admin users cannot be updated")

    update_data = new_data.model_dump(exclude_none=True) # Автоматический убирает None

    if "username" in update_data:
        result = await session.execute(
            select(UserModel).where(UserModel.username == update_data["username"])
        )
        user_with_same_username = result.scalars().first()

        if user_with_same_username and user_with_same_username.id != existing_user.id:
            raise HTTPException(status_code=409, detail="User already exists")

    for field, value in update_data.items():
        if field == "password":
            value = hash_password(value)
        setattr(existing_user, field, value)

    await session.commit()
    await session.refresh(existing_user)

    return existing_user


@admin_router.delete("/users/{user_id}",
                     response_model=UserReadSchema)
async def delete_user(
        session: SessionDep,
        user_id: int,
        admin: UserModel = Depends(get_current_admin)
):
    result = await session.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    existing_user = result.scalars().first()

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if existing_user.id == admin.id:
        raise HTTPException(status_code=400, detail="You cannot remove yourself")

    if existing_user.role == "admin":
        raise HTTPException(status_code=403, detail="Admin users cannot be deleted")

    await session.delete(existing_user)
    await session.commit()

    return existing_user