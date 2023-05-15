from flask_pydantic import validate
from flask_restx import Namespace, Resource

from src.app.api.user.controller import UserController
from src.app.api.base.utils import create_api_schema_model
from src.app.api.user.schema import User as UserSchema, UserCreate as UserCreateSchema, UserList as UserListSchema
api = Namespace("user", description="User Endpoint")

user_create = create_api_schema_model(api, UserCreateSchema)
# user_put = create_api_schema_model(api, UserPutSchema)
user_list = create_api_schema_model(api, UserListSchema)
user_schema = create_api_schema_model(api, UserSchema)
# user_with_app_schema = create_api_schema_model(api, UserWithApplicationSchema)

@api.route("/")
class UserGetList(Resource):

    @api.doc(model=user_list)
    @validate()
    def get(self):
        users = UserController().list()
        return UserListSchema.from_orm(users)

    @api.expect(user_create)
    @validate()
    def post(self, body: UserCreateSchema):
        user = UserController().create(body.dict())
        return UserSchema.from_orm(user)

@api.route("/<int:id>")
class UserGetById(Resource):

    @api.doc(model=user_schema)
    @validate()
    def get(self, id: int):
        user = UserController().get(id)
        return UserSchema.from_orm(user)
