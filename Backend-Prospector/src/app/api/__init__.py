from flask_restx import Api
from src.app.api.view import api as site_api
from src.app.api.user.view import api as user_api
from src.app.api.auth.view import api as auth_api
from src.app.api.analytics.view import api as analytics_api

api = Api(title="Siemens Green Energy Analytics", description="API for Analytics Platform")

api.add_namespace(site_api)
api.add_namespace(user_api)
api.add_namespace(auth_api)
api.add_namespace(analytics_api)
