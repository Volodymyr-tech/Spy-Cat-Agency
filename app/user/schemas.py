from pydantic import BaseModel, EmailStr, Field


class SUserRegister(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., min_length=5, max_length=50, description="Password from 1-50 chars")
    password_check: str = Field(..., min_length=5, max_length=50, description="Password from 1-50 chars")
    name: str = Field(..., min_length=3, max_length=50, description="Name  1-50 chars")


class SUserAuth(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., min_length=5, max_length=50, description="Password from 1-50 char")


class SUserRead(BaseModel):
    id: int = Field(..., description="Id user")
    name: str = Field(..., min_length=3, max_length=50, description="name from 1-50 chars")