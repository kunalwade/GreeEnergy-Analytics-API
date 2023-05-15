from flask_pydantic import validate

from flask_restx import Namespace, Resource

from src.app.api.base.utils import create_api_schema_model
from src.app.api.analytics.controller import AnalyticsController
from src.app.api.analytics.schema import AnalyticsCreate as AnalyticsCreateSchema, Analytics as AnalyticsSchema

api = Namespace("analytics", description="Analytics Endpoint")

analytics_schema = create_api_schema_model(api, AnalyticsSchema)
analytics_create_schema = create_api_schema_model(api, AnalyticsCreateSchema)

@api.route("/")
class AnalyticsGetList(Resource):

    @api.doc(model=analytics_schema)
    @api.expect(analytics_create_schema)
    @validate()
    def post(self, body: AnalyticsCreateSchema):
        analytics = AnalyticsController().create(body.dict())
        return AnalyticsSchema.from_orm(analytics)
    

@api.route('/<int:id>')
class AnalyticsGetById(Resource):
    @validate()
    def get(self, id:int):
        calculations = AnalyticsController().get_calculations(id)
        return AnalyticsSchema.from_orm(calculations)
