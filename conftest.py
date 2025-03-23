import requests
import pytest
import random
import string
import data.urls


@pytest.fixture
def create_and_delete_courier():
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = "".join(random.choice(letters) for i in range(length))
        return random_string

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(data.urls.Urls.COURIER_URL, json=payload)
    assert response.status_code == 201
    assert response.json()["ok"] is True

    yield {
        "login": login,
        "password": password,
        "firstName": first_name,
        "payload": payload
    }

    login_response = requests.post(data.urls.Urls.COURIER_LOGIN_URL, json=
    {
        "login": login,
        "password": password
    })
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]

        delete_response = requests.delete(f"{data.urls.Urls.COURIER_URL}/{courier_id}",
                                          json={"id": courier_id})
        assert delete_response.status_code == 200
        assert delete_response.json()["ok"] is True
