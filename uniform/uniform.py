from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis


class UniformService:
    name = "uniform_service"

    redis = Redis('development')
    github_rpc = RpcProxy('github_service')
    gitlab_rpc = RpcProxy('gitlab_service')

    @rpc
    def search(self, q):
        gitlab_repos = self.gitlab_rpc.search(q)
        github_repos = self.github_rpc.search(q)
        return {**gitlab_repos, **github_repos}
