from data.endpoints import Endpoints
from data.urls import Urls
from utilities.auth import Authentication
from utilities.clients import Clients


class Client:
    @staticmethod
    def get_client_data(client_id, valid_token=True):
        return Authentication.auth_header(valid_token).get(Urls.API + Endpoints.CLIENT + '/' + client_id)

    @staticmethod
    def update_client_data(client_id, updated_data, valid_token=True):
        return Authentication.auth_header(valid_token).put(url=Urls.API + Endpoints.CLIENT + '/' + client_id,
                                                           data=updated_data)

    @staticmethod
    def delete_client(client_id, valid_token=True):
        return Authentication.auth_header(valid_token).delete(Urls.API + Endpoints.CLIENT + '/' + client_id)

    @staticmethod
    def create_new_client(client_data, valid_token=True):
        return Authentication.auth_header(valid_token).post(Urls.API + Endpoints.CLIENT, data=client_data)

    @staticmethod
    def return_valid_client_id(valid_token=True):
        return Clients.get_client_list(valid_token).json()['clients'][0]['id']
