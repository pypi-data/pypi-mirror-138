from sanic.response import json
from sanic.views import HTTPMethodView

from insanic.http import HTTP_STATUS, Response
from insanic.serializers import Serializer

__all__ = (
    'View',
)


class View(HTTPMethodView):
    Response = Response  # Shortcut for typing

    serializer_class: Serializer | None = None

    def ok_response(self, data: dict, http_status=HTTP_STATUS.OK) -> Response:
        response_data = { 'status': 'ok', 'data': data }
        return json(response_data, status=http_status)

    def error_response(self, errors: dict, http_status=HTTP_STATUS.BAD_REQUEST) -> Response:
        response_data = { 'status': 'error', 'errors': errors }
        return json(response_data, status=http_status)

    async def serialized_response(self, data: any, serializer_class: Serializer=None, http_status=HTTP_STATUS.OK) -> Response:
        serializer_class = serializer_class or self.serializer_class
        if not serializer_class:
            raise NotImplementedError('Serializer class must be specified')

        serializer_kwargs = { 'many': isinstance(data, list) }
        serializer = serializer_class(**serializer_kwargs)
        serialized_data = await serializer.serialize(data)

        return self.ok_response(serialized_data, http_status=http_status)
