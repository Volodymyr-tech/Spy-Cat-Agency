from typing import List

from sqlalchemy import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select



class BaseCRUD:
    model = None


    @classmethod
    async def add(cls, session: AsyncSession , **values):
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance


    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession , data_id: int):
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    @classmethod
    async def find_one_or_none(cls, session: AsyncSession , **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()


    @classmethod
    async def find_all(cls,session: AsyncSession , **filter_by):
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

