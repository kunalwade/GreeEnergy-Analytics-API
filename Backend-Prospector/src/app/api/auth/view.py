# from flask import jsonify
from flask_restx import Namespace, Resource
from flask_pydantic import validate
# from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required

from src.app.api.auth.controller import AuthTokenController
from src.app.api.auth.schema import GetTokenSchema
from src.app.api.base.utils import create_api_schema_model

api = Namespace("auth", description="Auth Endpoint")
parser = api.parser()
parser.add_argument('Authorization', location='headers')

get_token_schema = create_api_schema_model(api, GetTokenSchema)


@api.route("/login")
class AuthGetToken(Resource):

    @api.expect(get_token_schema)
    @validate()
    def post(self, body: GetTokenSchema):
        token = AuthTokenController().get_token(body.dict())
        return token
