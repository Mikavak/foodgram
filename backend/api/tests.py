from django.test import TestCase


class TestRoutes(TestCase):

    def test_home_page(self):
        # Вызываем метод get для клиента (self.client)
        # и загружаем главную страницу.
        response = self.client.get('/')
        # Проверяем, что код ответа равен 200.
        self.assertEqual(response.status_code, 200)