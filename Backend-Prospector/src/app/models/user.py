from src.app.database import db
from src.app.models.generic_model import GenericModel
# from src.app.models.role import user_role_mapper_table

class User(GenericModel):
    __tablename__ = "user"
    email = db.Column(db.String(80))
    first_name = db.Column(db.String(40))
    last_name = db.Column(db.String(40))
    password = db.Column(db.String(255))

    sites = db.relationship("Site", back_populates="site_owner")
