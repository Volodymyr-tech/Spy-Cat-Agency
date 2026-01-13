from http.client import HTTPException
from typing import Annotated
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi import Depends, APIRouter
from pydantic.experimental.pipeline import validate_as_deferred
from sqlalchemy.ext.asyncio import AsyncSession

from app.cat.crud_cat import CatCrud
from app.cat.schemas import CatCreate
from app.core import db_helper
from app.mission.model import Mission
from app.target.model import Target
from app.user.dependencies import get_current_user
from app.user.model import User
from app.user.router import router
from app.core.jinja_templates import templates

router = APIRouter(prefix='/cats', tags=['cats'])

@router.get("/dashboard", response_class=HTMLResponse)
async def get_cats_dashboard_page(request: Request, current_user:Annotated[User, Depends(get_current_user)]):
    return templates.TemplateResponse("cats.html", {"request": request})

@router.get("/all")
async def get_all_cat_spy(session: Annotated[AsyncSession, Depends(db_helper.session_dependency)], current_user:Annotated[User, Depends(get_current_user)]):
    spy = await CatCrud.find_all(session=session)
    return spy


@router.post("/create")
async def create_cspy_cat(
        schema: CatCreate,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    validate_data = schema.model_dump()
    spy = await CatCrud.add(session=session, **validate_data)
    return spy



@router.get("/{cat_id}")
async def get_single_cat(
    cat_id: int,
    session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    cat = await CatCrud.find_one_or_none(id=cat_id, session=session)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat agent not found")
    return cat


@router.patch("/{cat_id}/salary")
async def update_cat_salary(
        cat_id: int,
        salary: float,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    cat = await CatCrud.find_one_or_none(id=cat_id, session=session)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat agent not found")

    # В твоем CRUD методе add/update должна быть поддержка изменения полей
    cat.salary = salary
    await session.commit()
    return {"status": "success", "new_salary": salary}


@router.delete("/{cat_id}/remove")
async def remove_spy_cat(
        cat_id: int,
        session: Annotated[AsyncSession, Depends(db_helper.session_dependency)],
        current_user: Annotated[User, Depends(get_current_user)]
):
    cat = await CatCrud.find_one_or_none(id=cat_id, session=session)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat agent not found")

    await session.delete(cat)
    await session.commit()
    return {"status": "agent removed"}