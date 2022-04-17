import pytest as pytest
from pyparsing import empty

from data.texts import Text
from data.user_data import UserData
from utilities.users import User
from utilities.client import Client
from http import HTTPStatus


@pytest.fixture()
def set_default_user():
    yield
    response = Client.update_client_data(client_id=Client.return_valid_client_id(),
                                         updated_data=User.generate_user_data(name=UserData.DEFAULT_FIRSTNAME,
                                                                              surname=UserData.DEFAULT_LASTNAME,
                                                                              phone_number=UserData.DEFAULT_PHONE))
    assert response.status_code == HTTPStatus.OK.value
    assert response.json()['id'] is not empty
    assert response.json()['firstName'] == UserData.DEFAULT_FIRSTNAME
    assert response.json()['lastName'] == UserData.DEFAULT_LASTNAME
    assert response.json()['phone'] == UserData.DEFAULT_PHONE


# New client is not visible on client's list
@pytest.mark.skip
def test_create_new_client():
    resp = Client.create_new_client(
        User.generate_user_data(UserData.VALID_FIRSTNAME, UserData.VALID_LASTNAME, UserData.VALID_PHONE))
    assert resp.status_code == HTTPStatus.OK.value
    assert resp.json()['id'] is not empty
    assert resp.json()['firstName'] == UserData.VALID_FIRSTNAME
    assert resp.json()['lastName'] == UserData.VALID_LASTNAME
    assert resp.json()['phone'] == UserData.VALID_PHONE


@pytest.mark.smoke
def test_create_new_client_without_first_name():
    resp = Client.create_new_client(User.generate_user_data('', UserData.VALID_LASTNAME, UserData.VALID_PHONE))
    assert resp.status_code == HTTPStatus.BAD_REQUEST.value
    assert resp.json()['message'] == Text.REQUIRED_FIRST_NAME


# Test give 200 and should give 400 as a result due to fact that phone number is mandatory field.
@pytest.mark.skip
def test_create_new_client_without_phone_number():
    resp = Client.create_new_client(User.generate_user_data(UserData.VALID_FIRSTNAME, UserData.VALID_LASTNAME, ''))
    assert resp.status_code == HTTPStatus.BAD_REQUEST.value
    assert resp.json()['message'] == Text.REQUIRED_LAST_NAME


@pytest.mark.smoke
def test_create_new_client_without_last_name():
    resp = Client.create_new_client(User.generate_user_data(UserData.VALID_FIRSTNAME, '', UserData.VALID_PHONE))
    assert resp.status_code == HTTPStatus.BAD_REQUEST.value
    assert resp.json()['message'] == Text.REQUIRED_LAST_NAME


@pytest.mark.smoke
def test_create_new_client_without_valid_token():
    resp = Client.create_new_client(
        client_data=User.generate_user_data(UserData.VALID_FIRSTNAME, '', UserData.VALID_PHONE),
        valid_token=False)
    assert resp.status_code == HTTPStatus.FORBIDDEN.value
    assert resp.json()['message'] == Text.API_KEY_ERROR


@pytest.mark.smoke
def test_delete_existing_user():
    resp = Client.delete_client(client_id=Client.return_valid_client_id())
    assert resp.status_code == HTTPStatus.OK.value
    assert resp.json()['message'] == Text.CLIENT_DELETED


@pytest.mark.system
def test_delete_not_existing_user():
    resp = Client.delete_client(client_id=UserData.NOT_EXISTING_ID)
    assert resp.status_code == HTTPStatus.NOT_FOUND.value
    assert resp.json()['message'] == Text.CLIENT_NOT_FOUND


@pytest.mark.smoke
def test_delete_client_without_valid_token():
    client_id = Client.return_valid_client_id()
    resp = Client.delete_client(client_id=client_id, valid_token=False)
    assert resp.status_code == HTTPStatus.FORBIDDEN.value
    assert resp.json()['message'] == Text.API_KEY_ERROR


# Put request does not update the first name field, TBD
@pytest.mark.skip
def test_update_existing_user(set_default_user):
    client_id = Client.return_valid_client_id()
    new_client_data = User.generate_user_data(name=UserData.VALID_FIRSTNAME, surname=UserData.VALID_LASTNAME,
                                              phone_number=UserData.VALID_PHONE)
    resp = Client.update_client_data(client_id=client_id, updated_data=new_client_data)

    assert resp.status_code == HTTPStatus.OK.value
    assert resp.json()['id'] == client_id
    assert resp.json()['lastName'] == UserData.VALID_LASTNAME
    assert resp.json()['phone'] == UserData.VALID_PHONE
    # assert resp.json()['firstName'] == UserData.VALID_USERNAME


@pytest.mark.smoke
def test_update_existing_user_without_name():
    client_id = Client.return_valid_client_id()
    new_client_data = User.generate_user_data(name='', surname=UserData.VALID_LASTNAME,
                                              phone_number=UserData.VALID_PHONE)
    resp = Client.update_client_data(client_id=client_id, updated_data=new_client_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json()['message'] == Text.REQUIRED_FIRST_NAME


@pytest.mark.smoke
def test_update_existing_user_without_surname():
    client_id = Client.return_valid_client_id()
    new_client_data = User.generate_user_data(name=UserData.VALID_FIRSTNAME, surname='',
                                              phone_number=UserData.VALID_PHONE)
    resp = Client.update_client_data(client_id=client_id, updated_data=new_client_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json()['message'] == Text.REQUIRED_LAST_NAME


@pytest.mark.smoke
def test_update_existing_user_without_phone_number():
    client_id = Client.return_valid_client_id()
    new_client_data = User.generate_user_data(name=UserData.VALID_FIRSTNAME, surname=UserData.VALID_LASTNAME,
                                              phone_number='')
    resp = Client.update_client_data(client_id=client_id, updated_data=new_client_data)

    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.json()['message'] == Text.REQUIRED_PHONE


@pytest.mark.system
def test_update_existing_user_without_valid_token():
    client_id = Client.return_valid_client_id()
    new_client_data = User.generate_user_data(name=UserData.VALID_FIRSTNAME, surname=UserData.VALID_LASTNAME,
                                              phone_number=UserData.VALID_PHONE)
    resp = Client.update_client_data(client_id=client_id, updated_data=new_client_data, valid_token=False)

    assert resp.status_code == HTTPStatus.FORBIDDEN.value
    assert resp.json()['message'] == Text.API_KEY_ERROR


@pytest.mark.smoke
def test_get_valid_user():
    client_id = Client.return_valid_client_id()
    resp = Client.get_client_data(client_id=client_id)

    assert resp.status_code == HTTPStatus.OK
    assert resp.json()['id'] == client_id
    assert resp.json()['firstName'] is not ''
    assert resp.json()['lastName'] is not ''
    assert resp.json()['phone'] is not ''


@pytest.mark.smoke
def test_get_not_existing_user():
    resp = Client.get_client_data(client_id=UserData.NOT_EXISTING_ID)

    assert resp.status_code == HTTPStatus.NOT_FOUND
    assert resp.json()['message'] == Text.CLIENT_NOT_FOUND


@pytest.mark.smoke
def test_get_existing_user_without_valid_token():
    resp = Client.get_client_data(client_id=Client.return_valid_client_id(), valid_token=False)

    assert resp.status_code == HTTPStatus.FORBIDDEN
    assert resp.json()['message'] == Text.API_KEY_ERROR


# Put request does not update the first name field, TBD
@pytest.mark.skip
def test_update_existing_user_with_too_long_name():
    client_id = Client.return_valid_client_id()
    new_client_data = User.generate_user_data(name=User.generate_random_characters(51), surname=UserData.VALID_LASTNAME,
                                              phone_number=UserData.VALID_PHONE)
    resp = Client.update_client_data(client_id=client_id, updated_data=new_client_data)


# Put request allows to update surname with more than 50 characters.
@pytest.mark.skip
def test_update_existing_user_with_too_long_surname():
    client_id = Client.return_valid_client_id()
    new_client_data = User.generate_user_data(name=UserData.VALID_FIRSTNAME,
                                              surname=User.generate_random_characters(51),
                                              phone_number=UserData.VALID_PHONE)
    resp = Client.update_client_data(client_id=client_id, updated_data=new_client_data)


# Put request allows to update phone number with more than 50 digits. TBD
@pytest.mark.skip
def test_update_existing_user_with_too_long_phone_number():
    client_id = Client.return_valid_client_id()
    new_client_data = User.generate_user_data(name=UserData.VALID_FIRSTNAME, surname=UserData.VALID_LASTNAME,
                                              phone_number=User.generate_random_phone_number(60))
    resp = Client.update_client_data(client_id=client_id, updated_data=new_client_data)


# Post request allows to create lastname with more than 50 characters, TBD
@pytest.mark.skip
def test_create_user_with_too_long_name():
    new_client_data = User.generate_user_data(name=User.generate_random_characters(51), surname=UserData.VALID_LASTNAME,
                                              phone_number=UserData.VALID_PHONE)
    resp = Client.create_new_client(client_data=new_client_data)


# Post request allows to create phone number with more than 50 digits, TBD
@pytest.mark.skip
def test_create_user_with_too_long_phone_number():
    new_client_data = User.generate_user_data(name=UserData.VALID_FIRSTNAME, surname=UserData.VALID_LASTNAME,
                                              phone_number=User.generate_random_phone_number(51))
    resp = Client.create_new_client(client_data=new_client_data)
