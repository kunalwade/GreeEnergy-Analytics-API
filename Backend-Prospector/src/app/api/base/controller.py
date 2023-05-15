from sqlalchemy import nullslast
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound

from src.app.database import db
from src.app.exception import BaseAPIException, ResourceNotFoundException


class BaseController:
    def __init__(self, model, db_session=None):
        self.model = model
        self.db_session = db_session if db_session else db.session

    def _generate_queryset(self):
        return self.db_session.query(self.model)

    def _generate_filter_by(self, *args, **kwargs):
        filter_by = {}
        return filter_by

    def _generate_filter(self, *args, **kwargs):
        return []

    def _get_default_order_by(self):
        return [self.model.id]

    def _parse_order_by_params(self, order_by_query_str: str):
        order_by = []
        for order_by_field in order_by_query_str.split(","):
            order_by_field = order_by_field.strip()
            if not order_by_field:
                continue

            is_descending = False
            if order_by_field[0] == "-":
                is_descending = True
                order_by_field = order_by_field[1:]

            model_attr = getattr(self.model, order_by_field, None)
            if model_attr:
                if is_descending:
                    model_attr = nullslast(model_attr.desc())
                order_by.append(model_attr)
        return order_by

    def _generate_order_by(self, *args, **kwargs):
        order_by = []
        if kwargs and kwargs.get("sort"):
            order_by = self._parse_order_by_params(kwargs.get("sort", ""))
        else:
            order_by = self._get_default_order_by()
        return order_by

    def get(self, id: int):
        """Retrieve record by id"""
        try:
            model = self.model.query.get_or_404(id)
            return model
        except NotFound:
            raise ResourceNotFoundException(
                details=f"{self.model.__name__} with id {id} not found"
            )

    def list(self, *args, **kwargs):
        """List records"""
        queryset = self._generate_queryset()
        filter_by = self._generate_filter_by(*args, **kwargs)
        filter_query = self._generate_filter(*args, **kwargs)
        order_by = self._generate_order_by(*args, **kwargs)
        model_list = (
            queryset.filter_by(**filter_by)
            .filter(*filter_query)
            .order_by(*order_by)
            .all()
        )
        return model_list

    def delete(self, id: int):
        """Delete record by id"""
        try:
            model = self.model.query.get_or_404(id)
            session = db.session()
            session.delete(model)
            session.commit()
            return model
        except NotFound:
            raise ResourceNotFoundException(
                details=f"{self.model.__name__} with id {id} not found"
            )

    def create(self, request_data):
        """Create record"""
        try:
            model = self.model(**request_data)
            session = db.session
            session.add(model)
            session.commit()
            return model
        except IntegrityError as e:
            # For violation of foreign key
            raise BaseAPIException(
                details=e.orig, code=400, message="Bad Request"
            )

    def patch(self, id, request_data):
        """Patch record"""
        try:
            session = db.session
            model = self.model.query.get_or_404(id)
            model.update(**request_data)
            session.commit()
            return model
        except NotFound:
            raise ResourceNotFoundException(
                details=f"{self.model.__name__} with id {id} not found"
            )
        except IntegrityError as e:
            # For violation of foreign key
            raise BaseAPIException(
                details=e.orig, code=400, message="Bad Request"
            )

    def put(self, id, request_data):
        try:
            session = db.session
            model = self.model.query.get_or_404(id)
            model.update(**request_data)
            session.commit()
            return model
        except NotFound:
            raise ResourceNotFoundException(
                details=f"{self.model.__name__} with id {id} not found"
            )
        except IntegrityError as e:
            # For violation of foreign key
            raise BaseAPIException(
                details=e.orig, code=400, message="Bad Request"
            )
