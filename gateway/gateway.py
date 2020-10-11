import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    uniform_rpc = RpcProxy('uniform_service')

    @http('GET', '/repos')
    def get_repos(self, request):
        headers = dict(request.headers)
        args = dict(request.args)

        result = self.uniform_rpc.search(headers, args)
        return json.dumps(
            {'repos': result}
        )
