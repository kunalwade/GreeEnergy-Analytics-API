from src.app.models.site import Site as SiteModel
from src.app.api.base.controller import BaseController
from src.app.api.analytics.controller import AnalyticsController
from src.app.models.analytics import Analytics
from src.app.database import db

class SiteController(BaseController):
    def __init__(self):
        super().__init__(SiteModel)

    def get_analysed_site_count(self):
        session = db.session()
        analysed_site_count = session.query(SiteModel).filter_by(is_analysed=True).count()
        unanalysed_site_count = session.query(SiteModel).filter_by(is_analysed=False).count()

        return{
            "Analysed_Site":{"count": analysed_site_count},
            "Unanalysed_Site":{"count": unanalysed_site_count},
        }

    def check_site_analytics(self, id):
        session = db.session()
        site = session.query(SiteModel).filter_by(id=id).one_or_none()
        if site:
            site_analytics = site.analytics
            if site_analytics:
                return site_analytics[0]
            else:
                latitude = site.latitude
                longitude = site.longitude
                site_area = site.site_area
        
                solar_power, getcarbonfootprint, getbreakeven  = AnalyticsController()._get_calculations(latitude, longitude, site_area)
                analytics = Analytics(site_id=site.id, solar_power=solar_power, carbonfootprint=getcarbonfootprint, breakeven=getbreakeven)
                session.add(analytics)
                site.update(is_analysed=True)
                session.commit()
                return analytics
            