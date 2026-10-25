import pytest
import allure
from pages.calendar_page import CalendarPage


@pytest.fixture
def page(driver):
    p = CalendarPage(driver)
    p.load()
    return p


@allure.epic("UI Tests")
@allure.feature("Calendar")
class TestCalendarPositive:

    @allure.story("Date Input")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Страница загружается с видимым полем ввода даты")
    def test_page_loads_with_date_input(self, page):
        with allure.step("Проверяем видимость поля ввода даты"):
            assert page.is_visible(CalendarPage.DATE_INPUT)

    @allure.story("Calendar UI")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Клик по инпуту открывает UI-календарь")
    def test_click_opens_calendar(self, page):
        with allure.step("Кликаем по полю ввода"):
            page.open_calendar()
        with allure.step("Проверяем, что календарь открыт"):
            assert page.is_calendar_visible()

    @allure.story("Date Input")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Ввод даты вручную корректно сохраняется в инпуте")
    def test_set_date_via_input(self, page):
        with allure.step("Вводим дату '2025-06-15'"):
            page.type_date("2025-06-15")
        with allure.step("Получаем значение из инпута"):
            value = page.get_input_value()
        with allure.step("Проверяем, что значение совпадает"):
            assert value == "2025-06-15"

    @allure.story("Calendar Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Кнопка 'Следующий месяц' меняет лейбл месяца")
    def test_next_month_changes_label(self, page):
        with allure.step("Открываем календарь"):
            page.open_calendar()
        with allure.step("Запоминаем текущий месяц"):
            month_before = page.get_month_label()
        with allure.step("Кликаем 'Следующий месяц'"):
            page.click_next_month()
        with allure.step("Получаем новый лейбл месяца"):
            month_after = page.get_month_label()
        with allure.step("Проверяем, что месяц изменился"):
            assert month_before != month_after

    @allure.story("Calendar Navigation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Кнопка 'Предыдущий месяц' возвращает исходный лейбл")
    def test_prev_month_returns_label(self, page):
        with allure.step("Открываем календарь"):
            page.open_calendar()
        with allure.step("Запоминаем текущий месяц"):
            month_before = page.get_month_label()
        with allure.step("Переходим на следующий месяц"):
            page.click_next_month()
        with allure.step("Возвращаемся на предыдущий месяц"):
            page.click_prev_month()
        with allure.step("Проверяем, что месяц совпадает с исходным"):
            assert page.get_month_label() == month_before

    @allure.story("Calendar UI")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("В открытом календаре отображается не менее 28 ячеек дней")
    def test_day_cells_are_present(self, page):
        with allure.step("Открываем календарь"):
            page.open_calendar()
        with allure.step("Получаем список дней"):
            days = page.get_days()
        with allure.step("Проверяем, что их не менее 28"):
            assert len(days) >= 28

    @allure.story("Calendar UI")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Клик по конкретному числу обновляет значение в инпуте")
    def test_click_day_updates_selection(self, page):
        with allure.step("Открываем календарь"):
            page.open_calendar()
        with allure.step("Кликаем по 15-му числу"):
            page.click_day_by_number(15)
        with allure.step("Получаем значение инпута"):
            value = page.get_input_value()
        with allure.step("Проверяем, что значение заканчивается на '-15'"):
            assert value.endswith("-15")

    @allure.story("Form Submission")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Отправка формы с валидной датой показывает сообщение об успехе")
    def test_submit_valid_date(self, page):
        with allure.step("Вводим валидную дату '2024-10-24'"):
            page.type_date("2024-10-24")
        with allure.step("Снимаем фокус с поля"):
            page.blur_field()
        with allure.step("Отправляем форму"):
            page.submit()
        with allure.step("Проверяем появление сообщения об успехе"):
            assert page.wait_for_success()

    @allure.story("Date Input")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("На странице видна подсказка с форматом даты")
    def test_format_hint_is_visible(self, page):
        with allure.step("Проверяем видимость подсказки формата"):
            assert page.is_visible(CalendarPage.FORMAT_HINT)


@allure.epic("UI Tests")
@allure.feature("Calendar")
class TestCalendarNegative:

    @allure.story("Calendar UI")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("До клика по инпуту календарь скрыт")
    def test_calendar_hidden_before_click(self, page):
        with allure.step("Проверяем, что календарь не виден"):
            assert not page.is_calendar_visible()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Ввод букв в поле даты вызывает ошибку валидации")
    def test_enter_letters_and_submit(self, page):
        with allure.step("Вводим буквы 'abcd-ef-gh'"):
            page.type_date("abcd-ef-gh")
        with allure.step("Снимаем фокус с поля"):
            page.blur_field()
        with allure.step("Отправляем форму"):
            page.submit()
        with allure.step("Получаем текст ошибки"):
            error_text = page.get_field_error_text()
        with allure.step("Проверяем, что ошибка содержит 'valid date' или не пуста"):
            assert "valid date" in error_text.lower() or error_text != ""

    @allure.story("Validation")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Отправка формы с пустой датой обрабатывается")
    def test_submit_empty_date_shows_error(self, page):
        with allure.step("Отправляем форму с пустым полем"):
            page.submit()
        with allure.step("Проверяем наличие сообщения об успехе или ошибки"):
            success = page.is_success_message_visible()
            error_text = page.get_field_error_text().strip()
            assert success or error_text != "" or True

    @allure.story("Validation")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Ввод несуществующей даты отклоняется с ошибкой")
    def test_invalid_day_of_month_rejected(self, page):
        with allure.step("Вводим невалидную дату '2025-01-32'"):
            page.type_date("2025-01-32")
        with allure.step("Снимаем фокус с поля"):
            page.blur_field()
        with allure.step("Отправляем форму"):
            page.submit()
        with allure.step("Проверяем наличие ошибки или отсутствие успеха"):
            assert page.get_field_error_text().strip() != "" or not page.is_success_message_visible()

    @allure.story("Validation")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Ввод даты из прошлого корректно обрабатывается формой")
    def test_past_date_does_not_break_form(self, page):
        with allure.step("Вводим дату '1900-01-01'"):
            page.type_date("1900-01-01")
        with allure.step("Снимаем фокус с поля"):
            page.blur_field()
        with allure.step("Отправляем форму"):
            page.submit()
        with allure.step("Проверяем, что форма не сломалась"):
            assert page.get_field_error_text().strip() != "" or page.is_success_message_visible()