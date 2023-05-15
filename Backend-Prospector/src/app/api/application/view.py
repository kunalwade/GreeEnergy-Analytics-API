from flask_pydantic import validate
from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required

from src.app.api.application.controller import ApplicationController
from src.app.api.base.utils import create_api_schema_model
from src.app.api.application.schema import Application, ApplicationWithUser, ApplicationListWithUser, ApplicationCreate, ApplicationPut
from src.app.api.application.schema import ApplicationList as ApplicationListSchema
from flask_jwt_extended import current_user
from src.app.api.auth.utils import permissions_required, roles_required

api = Namespace("application", description="Application Endpoint")

application_create = create_api_schema_model(api, ApplicationCreate)
application_put = create_api_schema_model(api, ApplicationPut)
application_list = create_api_schema_model(api, ApplicationListSchema)
application_schema = create_api_schema_model(api, Application)
application_with_user_schema = create_api_schema_model(api, ApplicationWithUser)
application_list_with_user_schema = create_api_schema_model(api, ApplicationListWithUser)

@api.route("/")
@api.doc(security=["accessToken"])
class ApplicationList(Resource):
    @api.doc(model=application_list_with_user_schema)
    @jwt_required()
    @permissions_required(["application:list"])
    @validate()
    def get(self):
        print(current_user)
        app_list = ApplicationController().list()
        return ApplicationListWithUser.from_orm(app_list)

    @api.expect(application_create)
    @api.doc(model=application_schema)
    @jwt_required()
    @permissions_required(["application:create"])
    @validate(on_success_status=201)
    def post(self, body: ApplicationCreate):
        request_data = body.dict()
        request_data.update({"application_owner_id": current_user.id})
        application = ApplicationController().create(request_data)
        return Application.from_orm(application)


@api.route("/<int:id>")
@api.doc(security=["accessToken"])
class ApplicationGetById(Resource):
    @api.doc(model=application_with_user_schema)
    @jwt_required()
    @permissions_required(["application:view"])
    @validate()
    def get(self, id: int):
        application = ApplicationController().get(id)
        return ApplicationWithUser.from_orm(application)

    @api.expect(application_put)
    @api.doc(model=application_schema)
    @jwt_required()
    @permissions_required(["application:edit"])
    @validate()
    def put(self, id: int, body: ApplicationPut):
        applcation = ApplicationController().put(id, body.dict())
        return Application.from_orm(applcation)
