from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnalyticsBase(BaseModel):
    solar_power:Optional[float]
    breakeven : Optional[float]
    carbonfootprint : Optional[float]

class Analytics(AnalyticsBase):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode=True


class AnalyticsCreate(BaseModel):
    site_id: int
