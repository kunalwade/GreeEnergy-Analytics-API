from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, validator

class SiteBase(BaseModel):
    site_name: str
    is_existing_project:bool
    latitude:float
    longitude:float
    site_area:float
    description:Optional[str]
    is_analysed:bool


class Site(SiteBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode=True

class SiteList(BaseModel):
    __root__:List[Site]

    class Config:
        orm_mode=True

class SiteCreate(SiteBase):
    pass

class SitePatch(BaseModel):
    site_name: Optional[str]
    is_existing_project:bool
    latitude:float
    longitude:float
    site_area:float
    description:Optional[str]
    # is_analysed: bool

    @validator("site_name")
    @classmethod
    def not_null(cls, v):
        if v is None:
            raise ValueError("Field cannot be null")
        return v
