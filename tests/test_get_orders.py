import allure
import requests
import data.urls


@allure.feature("Получение списка заказов")
class TestGetOrders:

    @allure.title("Проверяем, что возвращается список заказов")
    def test_get_orders_returns_list(self):
        response = requests.get(data.urls.Urls.CREATE_OR_GET_ORDER_URL)
        assert response.status_code == 200
        assert "orders" in response.json()