import pytest
import requests
import allure
import uuid
from urls import REGISTER_URL


@allure.feature("Регистрация пользователя")
@allure.tag("auth", "register")
class TestUserRegistration:

    @allure.title("Создание уникального пользователя с последующей очисткой")
    @allure.description("Проверяет, что можно зарегистрировать нового пользователя, и удаляет его после теста")
    def test_register_unique_user(self, created_user):
        with allure.step("Пользователь успешно создан через фикстуру"):
            # Внутри фикстуры уже проверено что status_code == 200 и success == True
            pass

        with allure.step("Проверяем наличие токенов в данных от фикстуры"):
            assert created_user["access_token"] is not None
            assert created_user["refresh_token"] is not None
            assert created_user["user"]["email"].startswith("test_")

    @allure.title("Попытка создать уже существующего пользователя")
    @allure.description("Проверяет, что сервер вернёт ошибку при повторной регистрации")
    def test_register_existing_user(self, created_user):
        with allure.step("Формируем payload с данными уже зарегистрированного пользователя"):
            payload = {
                "email": created_user["user"]["email"],
                "password": created_user["user"]["password"],
                "name": created_user["user"]["name"]
            }

        with allure.step("Отправляем POST-запрос"):
            response = requests.post(REGISTER_URL, json=payload)

        with allure.step("Проверяем, что получен 403 или 400"):
            assert response.status_code in [403, 400]

        with allure.step("Проверяем success=false"):
            data = response.json()
            assert data["success"] is False

    @allure.title("Регистрация без обязательного поля")
    @allure.description("Проверяет, что сервер отклонит запрос без поля name")
    def test_register_missing_required_field(self):
        with allure.step("Генерируем уникальный email"):
            random_id = str(uuid.uuid4())[:8]
            payload = {
                "email": f"missing_field_{random_id}@ya.ru",
                "password": "testpassword123"
            }

        with allure.step("Отправляем запрос без поля name"):
            response = requests.post(REGISTER_URL, json=payload)

        with allure.step("Проверяем код ответа"):
            assert response.status_code in [400, 403, 500]

        with allure.step("Проверяем success=false"):
            data = response.json()
            assert data["success"] is False