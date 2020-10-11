import requests
from nameko.rpc import rpc
from envyaml import EnvYAML

config = EnvYAML('config.yml')


class GitlabService:
    name = "gitlab_service"

    @rpc
    def search(self, gitlab_access_token, q):
        payload = {
            'scope': 'projects',
            'search': q
        }
        headers = {
            'PRIVATE-TOKEN': gitlab_access_token
        }
        r = requests.get(
            config['GITLAB_API'],
            params=payload,
            headers=headers
        )
        return r.json()
