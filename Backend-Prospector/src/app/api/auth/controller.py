# from src.app.models.site import Site as SiteModel
# from src.app.api.base.controller import BaseController
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import Unauthorized
from src.app.database import db
from src.app.models.user import User
from flask import jsonify
from src.app.api.auth.utils import hash_password
from src.app.jwt import jwt

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

class AuthTokenController():  

    def get_token(self, body: dict):

        user = self._get_user(body)
        additional_claims = {
            "aud": "siemens energy analytics",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email
        }
        access_token = create_access_token(user.id, additional_claims=additional_claims)
        return jsonify(access_token=access_token)
    
    def _get_user(self, body: dict):
        session = db.session()
        users = (
            session.query(User)
            .filter_by(
                email=body.get("email"),
                password=hash_password(body.get("password", ""))
            )
            .all()
        )
        if users and len(users) > 0:
            return users[0]
        raise Unauthorized(description="Incorrect Credentials")
