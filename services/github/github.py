import requests
from nameko.rpc import rpc
from envyaml import EnvYAML

config = EnvYAML('config.yml')


class GithubService:
    name = "github_service"

    @rpc
    def search(self, q):
        payload = {'q': q}
        r = requests.get(
            config['GITHUB_API'],
            params=payload
        )
        return r.json().get("items", [])

