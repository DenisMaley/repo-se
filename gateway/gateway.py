import json
from http import HTTPStatus

from nameko.rpc import RpcProxy
from nameko.web.handlers import HttpRequestHandler
from werkzeug.wrappers import Response
from nameko.exceptions import safe_for_serialization


class HttpError(Exception):
    error_code = 'BAD_REQUEST'
    status_code = HTTPStatus.BAD_REQUEST


class InvalidArgumentsError(HttpError):
    error_code = 'INVALID_ARGUMENTS'


class HttpEntrypoint(HttpRequestHandler):
    def response_from_exception(self, exc):
        if isinstance(exc, HttpError):
            response = Response(
                json.dumps({
                    'error': exc.error_code,
                    'message': safe_for_serialization(exc),
                }),
                status=exc.status_code,
                mimetype='application/json'
            )
            return response
        return HttpRequestHandler.response_from_exception(self, exc)


http = HttpEntrypoint.decorator


class GatewayService:
    name = 'gateway'

    uniform_rpc = RpcProxy('uniform_service')

    @http('GET', '/repos')
    def get_repos(self, request):
        headers = dict(request.headers)
        args = dict(request.args)

        if 'q' not in args:
            raise InvalidArgumentsError(
                "Argument `q` is required."
            )

        result = self.uniform_rpc.search(headers, args)
        response = Response(
            json.dumps({'repos': result}),
            status=HTTPStatus.OK,
            mimetype='application/json'
        )
        return response
