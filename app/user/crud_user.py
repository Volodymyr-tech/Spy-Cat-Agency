from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud_base import BaseCRUD
from app.user.model import User


class UserCrud(BaseCRUD):
    model = User



    @classmethod
    async def find_one_or_none_by_id(cls, id: int, session: AsyncSession):
        query = select(cls.model).filter_by(id=id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


