import json
import adapters
from nameko.rpc import rpc, RpcProxy
from nameko_redis import Redis
from nameko.testing.services import worker_factory


class UniformService:
    name = "uniform_service"

    redis = Redis('development')
    github_rpc = RpcProxy('github_service')
    gitlab_rpc = RpcProxy('gitlab_service')

    @rpc
    def search(self, headers, args):
        result = []

        q = args.get('q')

        github_repos = self.github_rpc.search(q)
        result += [
            GithubRepoAdapter().adapt(item).__dict__ for item in github_repos
        ]

        gitlab_access_token = headers.get('Gitlab-Access-Token')
        if gitlab_access_token:
            gitlab_repos = self.gitlab_rpc.search(gitlab_access_token, q)
            result += [
                GitlabRepoAdapter().adapt(item).__dict__ for item in gitlab_repos
            ]

        return result


class Repo(object):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.url = kwargs.get('url', None)


class GithubRepoAdapter(adapters.Adapter):
    class Meta(object):
        model = Repo

    name = adapters.CharField(source='full_name')
    url = adapters.CharField(source='html_url')


class GitlabRepoAdapter(adapters.Adapter):
    class Meta(object):
        model = Repo

    name = adapters.CharField(source='name_with_namespace')
    url = adapters.CharField(source='web_url')


# =============================================================================
# Begin test
# =============================================================================


def test_uniform_service():
    # create worker with mock dependencies
    service = worker_factory(UniformService)

    # add side effects to the mock proxy
    # to the "github_service" and "gitlab_service" services
    service.github_rpc.search.side_effect = [{'full_name': 'ama', 'html_url': 'zon'}]
    service.gitlab_rpc.search.side_effect = [{'name_with_namespace': 'goo', 'html_url': 'gle'}]

    # test adapters
    assert service.search(dict(), 'foo') == [{'name': 'ama', 'url': 'zon'}]
    service.github_rpc.search.assert_called_once_with('foo')
