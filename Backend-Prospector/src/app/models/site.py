from sqlalchemy import func
from src.app.database import db
from src.app.models.generic_model import GenericModel
from src.app.models.user import User

class Site(GenericModel):
    __tablename__ = "site"
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(50))
    is_existing_project = db.Column(db.Boolean)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    site_area = db.Column(db.Float)
    description = db.Column(db.String(100))
    is_analysed = db.Column(db.Boolean, default=False)
    site_owner_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete="CASCADE"), nullable=True)
    site_owner = db.relationship("User", back_populates="sites")
    analytics = db.relationship("Analytics", back_populates="site")