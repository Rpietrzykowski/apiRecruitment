import pytest

from data.texts import Text
from utilities.clients import Clients
from http import HTTPStatus


@pytest.mark.smoke
def test_get_valid_clients_list():
    resp = Clients.get_client_list()
    assert resp.status_code == HTTPStatus.OK
    assert len(resp.json()['clients']) >= 1, f"Number greater than 0 expected, got: {len(resp.json()['clients'])}"


@pytest.mark.smoke
def test_get_clients_list_without_valid_token():
    resp = Clients.get_client_list(valid_token=False)
    assert resp.status_code == HTTPStatus.FORBIDDEN
    assert resp.json()['message'] == Text.API_KEY_ERROR
