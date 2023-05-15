from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TimeStamps(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class BaseQuery(BaseModel):
    """
    Sort: Add mutliple sort fields in comma separated string.
          Use - (negative sign) for descending sort.
          E.g. sort=name,-created_at

    """

    sort: Optional[str] = Field(
        None,
        description="""Add mutliple sort fields in comma separated string.
          Use - (negative sign) for descending sort.
          E.g. sort=name,-created_at""",
    )
    filter_by: Optional[str] = Field(None, description="Filter By Field")


class ExcludeFieldsMixin(BaseModel):
    """
    This Mixin Class provides extended functionality for basemodel.
    Use: Exclude/hide schema fields when calling Model.schema() method
    """

    class Config:
        @classmethod
        def schema_extra(cls, schema, model) -> None:
            for exclude_field in model.__exclude_fields__:
                schema.get("properties", {}).pop(exclude_field)
