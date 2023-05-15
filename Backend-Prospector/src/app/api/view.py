# from flask import request
# from pylance import generate_jwt_token
# from flask_jwt import jwt, jwt_required
from flask_restx import Namespace, Resource
# from werkzeug.security import check_password_hash
from flask_pydantic import validate
from src.app.api.controller import SiteController
from src.app.api.schema import Site as SiteSchema
from src.app.api.schema import SiteList as SiteListSchema
from src.app.api.schema import SiteCreate as SiteCreateSchema
from src.app.api.schema import SitePatch as SitePatchSchema
from src.app.api.analytics.schema import Analytics as AnalyticsSchema
api = Namespace("site", description="CRUD operations for site")

site_create = api.schema_model(
    SiteCreateSchema.__name__, SiteCreateSchema.schema()
)
site_response = api.schema_model(SiteSchema.__name__, SiteSchema.schema())
site_list_response = api.schema_model(
    SiteListSchema.__name__, SiteListSchema.schema()
)
site_patch = api.schema_model(
    SitePatchSchema.__name__, SitePatchSchema.schema()
)
# site_analysis = api.schema_model(SiteSchema)

@api.route("/")
class ProjectDetails(Resource):
    """Site List and Create Endpoints"""
    @api.doc(model=site_list_response)
    @validate()
    def get(self):
        projects = SiteController().list()
        return SiteListSchema.from_orm(projects)

    @api.expect(site_create)
    @api.doc(model=site_response)
    @validate(on_success_status=201)
    def post(self, body: SiteCreateSchema):
        """Create Site"""
        project = SiteController().create(body.dict())
        return SiteSchema.from_orm(project)

@api.route('/<int:id>/analytics')
class SiteAnalytics(Resource):
    @validate()
    def get(self, id:int):
        site_calculations = SiteController().check_site_analytics(id)
        return AnalyticsSchema.from_orm(site_calculations)

@api.route('/<int:id>')
class ProjectById(Resource):
    @api.doc(model=site_response)
    @validate()
    def get(self, id: int):
        project = SiteController().get(id)
        return SiteSchema.from_orm(project)
    
    @api.doc(model=site_response)
    @validate()
    def delete(self, id: int):
        """Delete site method"""
        project = SiteController().delete(id)
        return SiteSchema.from_orm(project)

    @api.expect(site_patch)
    @api.doc(model=site_response)
    @validate()
    def patch(self, id: int, body: SitePatchSchema):
        """Patch card method"""
        project = SiteController().patch(id, body.dict(exclude_unset=True))
        return SiteSchema.from_orm(project)

@api.route('/statistics')
class ProjectAnalysis(Resource):
    """Route for analysed/ not analysed for projects"""
    @validate()
    def get(self):
        analysed_projects = SiteController().get_analysed_site_count()
        return analysed_projects



