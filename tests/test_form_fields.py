import pytest
import allure
from pages.form_fields_page import FormFieldsPage


@pytest.fixture
def page(driver):
    p = FormFieldsPage(driver)
    p.load()
    return p


@allure.epic("UI Tests")
@allure.feature("Form Fields")
class TestFormFieldsPositive:

    @allure.story("Automation Tools List")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Список 'Automation tools' содержит ровно 5 элементов")
    def test_automation_tools_list_has_5_items(self, page):
        with allure.step("Получаем список инструментов автоматизации"):
            tools = page.get_automation_tools_list()
        with allure.step("Проверяем, что их ровно 5"):
            assert len(tools) == 5
        with allure.step("Проверяем корректность содержимого"):
            assert tools == ["Selenium", "Playwright", "Cypress", "Appium", "Katalon Studio"]

    @allure.story("Form Submission")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Заполнение формы списком инструментов и отправка показывают алерт")
    def test_fill_message_with_automation_tools(self, page):
        with allure.step("Получаем текст списка инструментов"):
            tools_text = page.get_automation_tools_text()
        with allure.step("Проверяем, что список не пустой"):
            assert tools_text, "Список Automation Tools пуст"
        with allure.step("Проверяем, что элементы объединены запятой"):
            assert "," in tools_text, "Элементы не объединены запятой"
        with allure.step("Заполняем поле Name"):
            page.fill_name("Ivan Petrov")
        with allure.step("Заполняем поле Email"):
            page.fill_email("ivan@example.com")
        with allure.step("Заполняем поле Message списком инструментов"):
            page.fill_message(tools_text)
        with allure.step("Проверяем, что значение в поле Message совпадает"):
            assert page.get_message_value() == tools_text
        with allure.step("Отправляем форму"):
            page.submit()
        with allure.step("Ожидаем появления браузерного алерта"):
            alert = page.wait.until(
                __import__(
                    "selenium.webdriver.support.expected_conditions",
                    fromlist=["alert_is_present"],
                ).alert_is_present()
            )
        with allure.step("Проверяем текст алерта"):
            assert alert.text == "Message received!"
        with allure.step("Принимаем алерт"):
            alert.accept()