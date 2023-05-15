from src.app.database import db
from sqlalchemy import func

from src.app.database import db

class GenericModel(db.Model):
    __abstract__ = True
    # __table_args__ = {"schema": DB_SCHEMA}
    id = db.Column(
        db.Integer,
        nullable=False,
        primary_key=True,
        autoincrement=True,
        doc="Id of the database model",
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now(),
        doc="Created at timestamp",
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        onupdate=func.now(),
        doc="Updated at timestamp",
    )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
