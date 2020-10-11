import json
import adapters
from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis


class UniformService:
    name = "uniform_service"

    redis = Redis('development')
    github_rpc = RpcProxy('github_service')
    gitlab_rpc = RpcProxy('gitlab_service')

    @rpc
    def search(self, q):
        github_repos = self.github_rpc.search(q)
        norm_github_repos = [
            GithubRepoAdapter().adapt(item).__dict__ for item in github_repos
        ]

        gitlab_repos = self.gitlab_rpc.search(q)

        return norm_github_repos
        # return [*norm_github_repos, *norm_gitlab_repos]


class Repo(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.url = kwargs.get('url', None)


class GithubRepoAdapter(adapters.Adapter):
    class Meta(object):
        model = Repo

    name = adapters.CharField(source='full_name')
    url = adapters.CharField(source='html_url', default='')
