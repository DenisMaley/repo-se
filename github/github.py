from nameko.rpc import rpc


class GithubService:
    name = "github_service"

    @rpc
    def search(self, q):
        return {'github': q}
