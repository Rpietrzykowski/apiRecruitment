import requests
from data.urls import Urls
from data.endpoints import Endpoints
from data.user_data import UserData


class Authentication:
    @staticmethod
    def get_user_token(username=UserData.LOGIN, passwd=UserData.PASSWD):
        try:
            resp = requests.post(url=Urls.API + Endpoints.TOKEN, auth=(username, passwd))
            resp.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        return resp

    @staticmethod
    def get_token_with_invalid_credentials(username=UserData.INVALID_LOGIN, passwd=UserData.INVALID_PASSWORD):
        return requests.post(url=Urls.API + Endpoints.TOKEN, auth=(username, passwd))

    @staticmethod
    def auth_header(valid=True):
        session = requests.Session()
        if valid is True:
            session.headers.update({
                'X-API-KEY': Authentication.get_user_token().json()['key'],
                'Content-Type': 'application/json'
            })
        else:
            session.headers.update({
                'X-API-KEY': 'invalid token',
                'Content-Type': 'application/json'
            })

        return session
