from typing import Optional, List
from pydantic import BaseModel
from src.app.api.base.schema import TimeStamps

class ApplicationBase(BaseModel):
    name: str
    description: Optional[str]
    information_classification: Optional[str]
    status: Optional[str]

class Application(ApplicationBase, TimeStamps):
    id: int
    class Config:
        orm_mode = True

class ApplicationWithUser(Application):
    application_owner: Optional["User"]
    connection_sequences: List["NetworkConnectionSequence"]

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationList(BaseModel):
    __root__: List[Application]
    class Config:
        orm_mode = True

class ApplicationListWithUser(ApplicationList):
    __root__: List[ApplicationWithUser]


class ApplicationPut(ApplicationBase):
    class Config:
        orm_mode = True

# from easyaudit_backend.api.connection_sequence.schema import NetworkConnectionSequence
from src.app.models.generic_model import User
ApplicationWithUser.update_forward_refs()
