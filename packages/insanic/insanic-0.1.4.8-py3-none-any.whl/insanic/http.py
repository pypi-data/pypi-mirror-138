from http import HTTPStatus as HTTP_STATUS

from sanic.response import HTTPResponse

__all__ = (
    'HTTP_STATUS',
    'Response',
)


class Response(HTTPResponse):
    pass
