import json

from nameko.rpc import RpcProxy
from nameko.web.handlers import http


class GatewayService:
    name = 'gateway'

    uniform_rpc = RpcProxy('uniform_service')

    @http('GET', '/repos')
    def get_repos(self, request):
        q = request.args.get('q')
        result = self.uniform_rpc.search(q)
        return json.dumps(
            {'repos': result}
        )
