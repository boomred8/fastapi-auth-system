from authx import AuthX, AuthXConfig
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from src.database import SessionDep
from src.models import UserModel
from src.take_env import secret_key


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

config = AuthXConfig()
config.JWT_SECRET_KEY = secret_key
config.JWT_TOKEN_LOCATION=["headers"]

security = AuthX(config=config)

async def get_current_user(
        session: SessionDep,
        token: str = Depends(oauth2_scheme)
):
    try:
        payload = security._decode_token(token)
        user_id = payload.sub

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except Exception as e:
        print("VERIFY ERROR:", e)
        raise HTTPException(status_code=401, detail="Invalid token") from e

    result = await session.execute(
        select(UserModel).where(UserModel.id == int(user_id))
    )

    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive")

    return user

async def get_current_admin(
        current_admin: str = Depends(get_current_user)
):
    if current_admin.role != "admin":
        raise HTTPException(status_code=403, detail="User is not admin")
    return current_admin



