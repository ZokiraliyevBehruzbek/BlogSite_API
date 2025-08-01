from pydantic import BaseModel
from typing import Optional


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    is_superuser: Optional[bool] = False


class LoginSchema(BaseModel):
    username: str
    password: str


class GetSchema(BaseModel):
    user_id: int  # Super user idsini kiriting
    id: int


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    is_superuser: bool

    class Config:
        from_attributes = True

class ResetPasswordSchema(BaseModel):
    old_password: str
    new_password: str