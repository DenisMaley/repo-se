from nameko.rpc import rpc


class GitlabService:
    name = "gitlab_service"

    @rpc
    def search(self, q):
        return {'gitlab': q}
