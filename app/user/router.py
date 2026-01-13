from typing import List, Annotated

from fastapi import APIRouter, Response, Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_helper import db_helper
from app.core.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, PasswordMismatchException
from app.user.auth import get_password_hash, authenticate_user, create_access_token
from app.user.crud_user import UserCrud


from app.user.schemas import SUserRegister, SUserAuth, SUserRead
from app.core.jinja_templates import templates

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.get("/", response_class=HTMLResponse, name="auth_page")
async def get_auth(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@router.post("/register/", name="auth_register")
async def register_user(user_data: SUserRegister, session: Annotated[AsyncSession, Depends(db_helper.session_dependency)] ) -> dict:
    user = await UserCrud.find_one_or_none(email=user_data.email, session=session)

    if user:
        raise UserAlreadyExistsException

    if user_data.password != user_data.password_check:
        raise PasswordMismatchException("wrong password")

    hashed_password = get_password_hash(user_data.password)

    await UserCrud.add(session=session,
        username=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password
    )

    return {'message': 'Nicely done, you are registered now'}


@router.post("/login/", name="auth_login")
async def auth_user(response: Response, user_data: SUserAuth, session: Annotated[AsyncSession, Depends(db_helper.session_dependency)]):
    check = await authenticate_user(email=user_data.email, password=user_data.password, session=session)
    if check is None:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(check.id)})
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {'ok': True, 'access_token': access_token, 'refresh_token': None, 'message': 'You are authorized'}


@router.post("/logout/", name="auth_logout")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {'message': 'Session successfully logged out'}

