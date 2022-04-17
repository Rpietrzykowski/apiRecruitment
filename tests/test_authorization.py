import pytest

from http import HTTPStatus
from pyparsing import empty

from data.user_data import UserData
from utilities.auth import Authentication
from data.texts import Text


@pytest.mark.smoke
def test_auth_token_with_valid_user():
    resp = Authentication.get_user_token()
    assert resp.status_code == HTTPStatus.OK
    assert resp.json()['key'] is not empty


@pytest.mark.smoke
def test_auth_token_with_invalid_username_and_password():
    resp = Authentication.get_token_with_invalid_credentials()
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json()['message'] == Text.INVALID_CREDENTIALS


@pytest.mark.smoke
def test_auth_token_with_invalid_password():
    resp = Authentication.get_token_with_invalid_credentials(username=UserData.LOGIN)
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json()['message'] == Text.INVALID_CREDENTIALS


@pytest.mark.smoke
def test_auth_token_with_empty_username():
    resp = Authentication.get_token_with_invalid_credentials(username='')
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json()['message'] == Text.INVALID_CREDENTIALS


@pytest.mark.smoke
def test_auth_token_with_empty_password():
    resp = Authentication.get_token_with_invalid_credentials(passwd='')
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json()['message'] == Text.INVALID_CREDENTIALS


@pytest.mark.smoke
def test_auth_token_with_empty_username_and_password():
    resp = Authentication.get_token_with_invalid_credentials(username='', passwd='')
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json()['message'] == Text.INVALID_CREDENTIALS
