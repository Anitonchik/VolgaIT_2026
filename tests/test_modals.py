import pytest
import allure
from pages.modals_page import ModalsPage


@pytest.fixture
def page(driver):
    p = ModalsPage(driver)
    p.load()
    return p


@allure.epic("UI Tests")
@allure.feature("Modals")
class TestModalsPositive:

    @allure.story("Simple Modal")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Простое модальное окно открывается по клику на кнопку")
    def test_simple_modal_opens(self, page):
        with allure.step("Кликаем по кнопке открытия простого модала"):
            page.open_simple_modal()
        with allure.step("Проверяем, что модальное окно стало видимым"):
            assert page.is_simple_modal_visible()

    @allure.story("Simple Modal")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Простое модальное окно закрывается по клику на крестик")
    def test_simple_modal_closes(self, page):
        with allure.step("Открываем простое модальное окно"):
            page.open_simple_modal()
        with allure.step("Закрываем модальное окно"):
            page.close_simple_modal()
        with allure.step("Проверяем, что окно больше не видимо"):
            assert not page.is_simple_modal_visible()

    @allure.story("Form Modal")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Модальное окно с формой открывается по клику на кнопку")
    def test_form_modal_opens(self, page):
        with allure.step("Кликаем по кнопке открытия модала с формой"):
            page.open_form_modal()
        with allure.step("Проверяем, что модальное окно стало видимым"):
            assert page.is_form_modal_visible()

    @allure.story("Form Modal")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Поля формы принимают и удерживают введённые значения")
    def test_form_fields_accept_input(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Заполняем поля Name, Email, Message"):
            page.fill_form(name="Ivan", email="ivan@test.com", message="Hello")
        with allure.step("Проверяем значение поля Name"):
            assert page.get_input_value(ModalsPage.NAME_INPUT) == "Ivan"
        with allure.step("Проверяем значение поля Email"):
            assert page.get_input_value(ModalsPage.EMAIL_INPUT) == "ivan@test.com"
        with allure.step("Проверяем значение поля Message"):
            assert page.get_input_value(ModalsPage.MESSAGE_INPUT) == "Hello"

    @allure.story("Form Modal")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Очистка формы сбрасывает все поля в пустые строки")
    def test_clear_form_resets_fields(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Заполняем форму"):
            page.fill_form(name="Ivan", email="ivan@test.com", message="Hello")
        with allure.step("Очищаем форму"):
            page.clear_form()
        with allure.step("Проверяем, что поле Name пустое"):
            assert page.get_input_value(ModalsPage.NAME_INPUT) == ""
        with allure.step("Проверяем, что поле Email пустое"):
            assert page.get_input_value(ModalsPage.EMAIL_INPUT) == ""
        with allure.step("Проверяем, что поле Message пустое"):
            assert page.get_input_value(ModalsPage.MESSAGE_INPUT) == ""

    @allure.story("Form Submission")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Отправка валидной формы показывает сообщение об успехе")
    def test_submit_valid_form_shows_success(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Заполняем форму валидными данными"):
            page.fill_form(
                name="Ivan Petrov",
                email="ivan@example.com",
                message="Test message",
            )
        with allure.step("Отправляем форму"):
            page.submit_form()
        with allure.step("Проверяем появление сообщения об успехе"):
            assert page.is_success_visible()

    @allure.story("Form Modal")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Кнопка Submit в модальном окне активна по умолчанию")
    def test_submit_button_is_enabled(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Проверяем, что кнопка Submit активна"):
            assert page.is_submit_button_enabled()

    @allure.story("Form Modal")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Кнопка закрытия корректно скрывает модальное окно с формой")
    def test_form_modal_close_button_works(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Закрываем модальное окно"):
            page.close_form_modal()
        with allure.step("Проверяем, что окно больше не видимо"):
            assert not page.is_form_modal_visible()

    @allure.story("Form Modal")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Поле Message принимает длинное сообщение (500 символов)")
    def test_long_message_is_accepted(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Формируем длинное сообщение"):
            long_msg = "A" * 500
        with allure.step("Заполняем форму с длинным сообщением"):
            page.fill_form(name="Ivan", email="ivan@test.com", message=long_msg)
        with allure.step("Проверяем, что значение в поле Message совпадает"):
            assert page.get_input_value(ModalsPage.MESSAGE_INPUT) == long_msg


@allure.epic("UI Tests")
@allure.feature("Modals")
class TestModalsNegative:

    @allure.story("Simple Modal")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Простое модальное окно не отображается до клика на кнопку")
    def test_simple_modal_not_visible_before_click(self, page):
        with allure.step("Проверяем, что простое модальное окно скрыто"):
            assert not page.is_simple_modal_visible()

    @allure.story("Form Modal")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Модальное окно с формой не отображается до клика на кнопку")
    def test_form_modal_not_visible_before_click(self, page):
        with allure.step("Проверяем, что модальное окно с формой скрыто"):
            assert not page.is_form_modal_visible()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Отправка пустой формы вызывает ошибку валидации")
    def test_submit_empty_form_shows_error(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Отправляем пустую форму"):
            page.submit_form()
        with allure.step("Проверяем появление ошибки"):
            assert page.is_form_error_visible() or page.get_name_error_text() != ""

    @allure.story("Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Отправка формы без имени вызывает ошибку под полем Name")
    def test_submit_without_required_name(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Заполняем только Email и Message"):
            page.fill_form(email="test@test.com", message="msg")
        with allure.step("Отправляем форму"):
            page.submit_form()
        with allure.step("Проверяем появление ошибки под полем Name"):
            assert page.get_name_error_text() != "" or page.is_form_error_visible()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Отправка формы с невалидным email вызывает ошибку валидации")
    def test_submit_invalid_email_shows_error(self, page):
        with allure.step("Открываем модальное окно с формой"):
            page.open_form_modal()
        with allure.step("Заполняем форму с некорректным email"):
            page.fill_form(name="Ivan", email="not-an-email", message="msg")
        with allure.step("Отправляем форму"):
            page.submit_form()
        with allure.step("Проверяем появление ошибки email"):
            assert page.get_email_error_text() != "" or page.is_form_error_visible()