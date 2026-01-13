from typing import Annotated

from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core import db_helper
from app.core.config import get_auth_data

from app.core.exceptions import TokenExpiredException, NoJwtException, NoUserIdException, TokenNoFoundException

from app.user.crud_user import UserCrud



def get_token(request: Request):
    token = request.cookies.get('users_access_token')
    if not token:
        raise TokenNoFoundException
    return token


async def get_current_user(session: Annotated[AsyncSession, Depends(db_helper.session_dependency)], token: str = Depends(get_token)):
    try:
        auth_data = get_auth_data()
        payload = jwt.decode(token, auth_data['secret_key'], algorithms=auth_data['algorithm'])
    except JWTError:
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UserCrud.find_one_or_none_by_id(session=session, id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user