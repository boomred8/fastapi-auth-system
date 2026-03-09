import asyncio
from sqlalchemy import select

from src.database import async_session
from src.models import UserModel
from src.authorization import hash_password

async def create_admin():
    async with async_session() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.username == "admin")
        )
        user = result.scalars.first()

        if user:
            print("admin already exists")
            return

        admin = UserModel(
            username="admin",
            password=hash_password('admin123456'),
            role="admin",
            is_acive=True
        )

        session.add(admin)
        await session.commit()
        print('admin created successfully')

if __name__ == '__main__':
    asyncio.run(create_admin())