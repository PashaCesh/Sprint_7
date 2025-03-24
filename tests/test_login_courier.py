import allure
import requests
import pytest
import data.urls


@allure.feature("Авторизация курьером")
class TestLoginCourier:

    @allure.title("Проверяем, что курьером можно залогиниться")
    def test_courier_can_login(self, create_and_delete_courier):
        login_data = {
            "login": create_and_delete_courier["login"],
            "password": create_and_delete_courier["password"]
        }
        response = requests.post(data.urls.Urls.COURIER_LOGIN_URL, json=login_data)
        assert response.status_code == 200
        assert "id" in response.json()

    @allure.title("Проверяем, что нельзя залогиниться, если передать некорректный пароль")
    def test_login_with_incorrect_credentials(self, create_and_delete_courier):
        login_data = {
            "login": create_and_delete_courier["login"],
            "password": create_and_delete_courier["password"] + "password"
        }
        response = requests.post(data.urls.Urls.COURIER_LOGIN_URL, json=login_data)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Проверяем, что возвращается корректная ошибка, если не передавать одно из полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_without_missing_field(self, create_and_delete_courier, missing_field):
        login_data = {
            "login": create_and_delete_courier["login"],
            "password": create_and_delete_courier["password"]
        }
        del login_data[missing_field]
        response = requests.post(data.urls.Urls.COURIER_LOGIN_URL, json=login_data)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Проверяем, что нельзя залогиниться кредами несуществующего курьера")
    def test_login_with_nonexistent_credentials(self, create_and_delete_courier):
        login_data = {
            "login": "nonexistent_login",
            "password": "nonexistent_password"
        }
        response = requests.post(data.urls.Urls.COURIER_LOGIN_URL, json=login_data)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
