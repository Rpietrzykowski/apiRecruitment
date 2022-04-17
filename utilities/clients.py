from data.endpoints import Endpoints
from data.urls import Urls
from utilities.auth import Authentication


class Clients:
    @staticmethod
    def get_client_list(valid_token=True):
        return Authentication.auth_header(valid_token).get(url=Urls.API + Endpoints.CLIENTS)
