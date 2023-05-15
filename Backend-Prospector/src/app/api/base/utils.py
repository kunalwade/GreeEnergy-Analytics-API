from flask_restx import Namespace


def create_api_schema_model(api: Namespace, model):
    return api.schema_model(model.__name__, model.schema())


def create_api_params(model):
    return model.schema().get("properties")
