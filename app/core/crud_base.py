from typing import List

from sqlalchemy import Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select



class BaseCRUD:
    model = None

    # @classmethod
    # async def get_all(cls, session: AsyncSession) -> List[model]:
    #     stmt = select(cls.model).order_by(
    #         cls.model.id
    #     )
    #     result: Result = await session.execute(stmt)
    #     all_data = result.scalars().all()
    #     if (
    #         all_data is not None
    #     ):
    #         return list(all_data)
    #     else:
    #         return []


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


    # @classmethod
    # async def update(
    #         cls,
    #         session: AsyncSession,
    #         task_id: int,
    #         owner_id: int,
    #         update_data: dict,
    # ) -> TaskHumanTempalte:
    #
    #
    #     task = await cls.get_by_id(task_id=task_id, owner_id=owner_id, session=session)
    #
    #     if task is None:
    #         log.error(f"Task {task_id} not found")
    #         raise ValueError("Task not found")
    #
    #     for key, value in update_data.items():
    #         if hasattr(task, key):
    #             setattr(task, key, value)
    #
    #     await session.flush()  # Или commit(), если это финальное действие в роуте
    #     await session.refresh(task)
    #     return task
