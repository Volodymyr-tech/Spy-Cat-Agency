from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.db_helper import db_helper
from app.cat.model import Cat
from app.mission.model import Mission
from app.mission.schemas import MissionCreate
from app.target.model import Target
from app.user.dependencies import get_current_user
from app.user.model import User

router = APIRouter(prefix='/missions', tags=['Missions'])


@router.get("/all")
async def list_missions(
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        user: Annotated[User, Depends(get_current_user)]
):
    result = await session.execute(select(Mission).options(selectinload(Mission.targets)))
    return result.scalars().all()


@router.post("/create")
async def create_mission(
        schema: MissionCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        user: Annotated[User, Depends(get_current_user)]
):
    new_mission = Mission(is_completed=False)
    session.add(new_mission)
    await session.flush()

    for t_data in schema.targets:
        target = Target(mission_id=new_mission.id, **t_data.model_dump())
        session.add(target)

    await session.commit()
    return {"status": "created", "mission_id": new_mission.id}


@router.delete("/{mission_id}")
async def delete_mission(
        mission_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        user: Annotated[User, Depends(get_current_user)]
):
    mission = await session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(404, "Mission not found")

    if mission.cat_id:
        raise HTTPException(400, "Cannot delete mission assigned to a cat")

    await session.delete(mission)
    await session.commit()
    return {"ok": True}


@router.patch("/{mission_id}/assign/{cat_id}")
async def assign_cat(
        mission_id: int,
        cat_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        user: Annotated[User, Depends(get_current_user)]
):
    mission = await session.get(Mission, mission_id)
    cat = await session.get(Cat, cat_id)

    if not mission or not cat:
        raise HTTPException(404, "Mission or Cat not found")


    existing_mission = await session.execute(select(Mission).where(Mission.cat_id == cat_id))
    if existing_mission.scalar_one_or_none():
        raise HTTPException(400, "This cat is already on a mission")

    mission.cat_id = cat_id
    await session.commit()
    return {"status": "cat assigned"}


@router.patch("/target/{target_id}/notes")
async def update_notes(
        target_id: int,
        notes: str,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        user: Annotated[User, Depends(get_current_user)]
):
    target = await session.get(Target, target_id)
    if not target: raise HTTPException(404, "Target not found")

    mission = await session.get(Mission, target.mission_id)


    if target.is_completed or mission.is_completed:
        raise HTTPException(400, "Notes are frozen! Target or Mission is completed.")

    target.notes = notes
    await session.commit()
    return {"status": "notes updated"}


@router.patch("/target/{target_id}/complete")
async def complete_target(
        target_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        user: Annotated[User, Depends(get_current_user)]
):
    target = await session.get(Target, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    target.is_completed = True

    stmt = (
        select(Mission)
        .where(Mission.id == target.mission_id)
        .options(selectinload(Mission.targets))
    )
    result = await session.execute(stmt)
    mission = result.scalar_one_or_none()


    if all(t.is_completed for t in mission.targets):
        mission.is_completed = True

    await session.commit()
    return {"response": "ok"}


@router.get("/{mission_id}")
async def get_single_mission(
        mission_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        user: Annotated[User, Depends(get_current_user)]
):
    stmt = (
        select(Mission)
        .where(Mission.id == mission_id)
        .options(selectinload(Mission.targets))
    )
    result = await session.execute(stmt)
    mission = result.scalar_one_or_none()

    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    return mission