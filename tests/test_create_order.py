import allure
import pytest
import requests
import data.urls


@allure.title("Создание заказа")
class TestCreateOrder:

    @allure.title("Проверяем, что заказ создаётся с разными цветами или без цвета")
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    def test_create_order_with_color(self, color):

        payload = {
            "firstName": "Naruto",
            "lastName": "Uzumaki",
            "address": "Konoha, 12",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2024-01-05",
            "comment": "Saske, come back to Konoha",
            "color": color
        }
        response = requests.post(data.urls.Urls.CREATE_OR_GET_ORDER_URL, json=payload)
        assert response.status_code == 201
        assert "track" in response.json()
