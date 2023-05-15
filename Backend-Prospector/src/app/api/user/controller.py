from src.app.api.base.controller import BaseController
from src.app.models.user import User as UserModel
from src.app.api.auth.utils import hash_password

class UserController(BaseController):
    def __init__(self):
        super().__init__(UserModel)

    def create(self, request_data):
        request_data["password"] = hash_password(request_data["password"])
        return super().create(request_data)
