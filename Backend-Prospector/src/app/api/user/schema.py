from typing import Optional, List
from pydantic import BaseModel
from src.app.api.base.schema import TimeStamps

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class User(UserBase, TimeStamps):
    id: int
    class Config:
        orm_mode = True

# class UserWithApplication(User):
#     applications : List["Application"]

class UserCreate(UserBase):
    password: str

class UserList(BaseModel):
    __root__: List[User]
    class Config:
        orm_mode = True

class UserPut(UserBase):
    password: str
    class Config:
        orm_mode = True

# from src.app.api.application.schema import Application
# UserWithApplication.update_forward_refs()
