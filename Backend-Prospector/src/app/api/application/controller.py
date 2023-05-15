from src.app.api.base.controller import BaseController
from src.app.api.application import Application as ApplicationModel


class ApplicationController(BaseController):
    def __init__(self):
        super().__init__(ApplicationModel)
