from fastapi import status, HTTPException


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )


class TokenNoFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found"
        )


UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User already exists"
)

PasswordMismatchException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Bad password bro"
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong email o password"
)

NoJwtException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="bad token it is not valid"
)

NoUserIdException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Didnt find user id"
)

ForbiddenException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="You are unauthorized"
)
