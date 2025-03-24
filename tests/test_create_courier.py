import allure
import requests
import pytest
import data.urls


@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Проверяем, что курьер создаётся")
    def test_can_create_courier(self, create_and_delete_courier):
        response = create_and_delete_courier["response"]
        assert response.status_code == 201
        assert "ok" in response.json()

    @allure.title("Проверяем, что нельзя создать два одинаковых курьера")
    def test_cannot_create_duplicate_courier(self, create_and_delete_courier):
        payload = create_and_delete_courier["payload"]
        response = requests.post(data.urls.Urls.COURIER_URL, json=payload)
        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Проверяем, что возвращается корректная ошибка, если не передать одно из полей")
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_cannot_create_courier_without_required_field(self, create_and_delete_courier, missing_field):
        payload = create_and_delete_courier["payload"]
        del payload[missing_field]
        response = requests.post(data.urls.Urls.COURIER_URL, json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"
