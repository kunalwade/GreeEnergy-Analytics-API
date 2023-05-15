from src.app.models.generic_model import GenericModel
from src.app.database import db
from src.app.models.site import Site

class Analytics(GenericModel):
    __tablename__= "analytics"
    site_id = db.Column(db.Integer, db.ForeignKey(Site.id))
    solar_power = db.Column(db.Float)
    breakeven = db.Column(db.Float)
    carbonfootprint = db.Column(db.Float)
    
    site = db.relationship("Site", back_populates="analytics")
    