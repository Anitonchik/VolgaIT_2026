# Проект автоматизированного тестирования UI

Проект построен с использованием паттерна **Page Object Model (POM)** для обеспечения читаемости, переиспользования и легкой поддержки кода. В качестве тестового фреймворка используется **PyTest**, для взаимодействия с браузером — **Selenium WebDriver**, а для генерации отчётов — **Allure**.

---

## Архитектура проекта

Проект следует строгому разделению ответственности (Separation of Concerns) благодаря паттерну **Page Object Model**:

```text
project/
├── pages/                  # Page Objects (описание страниц, локаторов и методов)
│   ├── base_page.py        # Базовый класс с общими методами (открытие, клик, ввод, ожидания)
│   ├── ads_page.py         # Объект страницы "Ads" (Рекламные попапы)
│   ├── calendar_page.py    # Объект страницы "Calendar" (Календарь)
│   ├── form_fields_page.py # Объект страницы "Form Fields" (Поля формы)
│   └── modals_page.py      # Объект страницы "Modals" (Модальные окна)
├── tests/                  # Тестовые сценарии
│   ├── test_ads.py
│   ├── test_calendar.py
│   ├── test_form_fields.py
│   └── test_modals.py
├── conftest.py             # Фикстуры PyTest + хуки для скриншотов при падении
├── requirements.txt        # Зависимости проекта
└── README.md               # Документация проекта
```
---

## Стек технологий

| Технология | Назначение |
|---|---|
| **Python 3.10+** | Язык программирования |
| **Selenium WebDriver** | Инструмент автоматизации браузера |
| **PyTest** | Тестовый фреймворк |
| **Page Object Model** | Паттерн проектирования |
| **WebDriverWait + expected_conditions** | Явные ожидания для стабильности тестов |
| **Allure** | Генерация наглядных HTML-отчётов |

---

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/Anitonchik/VolgaIT_2026.git
cd VolgaIT_2026
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

`requirements.txt`:
```txt
selenium>=4.10.0
pytest>=7.4.0
allure-pytest>=2.13.0
```

### 3. Установка Allure CLI

- **macOS:** `brew install allure`
- **Windows:** `choco install allure`
- **Linux:** `sudo apt install allure`

### 4. Запуск всех тестов

```bash
pytest tests/
```

### 5. Запуск тестов для конкретной страницы

```bash
pytest tests/test_modals.py
pytest tests/test_calendar.py
pytest tests/test_ads.py
pytest tests/test_form_fields.py
```

### 6. Запуск с подробным выводом

```bash
pytest tests/ -v -s
```

---

## Настройка отчётов Allure

Отчёт Allure настроен в соответствии со следующими требованиями:

### Требование 1. Чёткое отображение запущенных тестов и их результатов

Реализовано через иерархическую структуру Allure:

| Уровень | Декоратор | Пример |
|---|---|---|
| `epic` | `@allure.epic` | "UI Tests" |
| `feature` | `@allure.feature` | "Modals", "Calendar", "Ads", "Form Fields" |
| `story` | `@allure.story` | "Simple Modal", "Form Validation", "Ad Popup" |
| `severity` | `@allure.severity` | `BLOCKER`, `CRITICAL`, `NORMAL`, `MINOR` |

В отчёте автоматически отображаются статусы: `passed`, `failed`, `broken`, `skipped`.

### Требование 2. Осмысленные названия тестов и шагов

- **Названия тестов** задаются через `@allure.title("Описание")`.
- **Шаги внутри теста** оборачиваются в `with allure.step("...")`, что позволяет видеть в отчёте последовательность действий.

Пример:
```python
@allure.title("Отправка формы с невалидным email вызывает ошибку валидации")
def test_submit_invalid_email_shows_error(self, page):
    with allure.step("Открываем модальное окно с формой"):
        page.open_form_modal()
    with allure.step("Заполняем форму с некорректным email"):
        page.fill_form(name="Ivan", email="not-an-email", message="msg")
    with allure.step("Отправляем форму"):
        page.submit_form()
    with allure.step("Проверяем появление ошибки email"):
        assert page.get_email_error_text() != ""
```

### Требование 3. Скриншоты при ошибках

Реализовано через pytest-хук `pytest_runtest_makereport` в `conftest.py`. При падении теста автоматически прикрепляются:
- **Скриншот** текущего состояния страницы (PNG).
- **HTML-код страницы** (для дополнительного дебага).

```python
import pytest
import allure


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver") or item.funcargs.get("page").driver
        if driver is not None:
            png = driver.get_screenshot_as_png()
            allure.attach(
                png,
                name=f"Screenshot_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
            html = driver.page_source.encode("utf-8")
            allure.attach(
                html,
                name=f"PageSource_{item.name}",
                attachment_type=allure.attachment_type.HTML,
            )
```

### Команды для работы с Allure

**Запуск тестов со сбором данных:**
```bash
pytest tests/ --alluredir=./allure-results --clean-alluredir
```

**Локальный просмотр отчёта:**
```bash
allure serve ./allure-results
```

**Генерация статического HTML-отчёта (для CI/CD):**
```bash
allure generate ./allure-results -o ./allure-report --clean
```

---

## Описание тестовых сценариев

Ниже представлено подробное описание автоматизированных тестовых сценариев, реализованных в проекте. Тесты разделены по страницам и типам (позитивные / негативные).

---

### 1. Страница "Ads" (Рекламные попапы)

**Файлы:** `pages/ads_page.py`, `tests/test_ads.py`
**URL:** `https://practice-automation.com/ads/`

#### Позитивные сценарии (`TestAdsPositive`)

| № | Название теста | Описание |
|---|---|---|
| 1 | `test_page_loads_with_title` | Страница успешно загружается и содержит заголовок "Ads". |
| 2 | `test_ad_appears_automatically` | Рекламный попап автоматически появляется на странице в течение 15 секунд. |
| 3 | `test_ad_has_title` | Попап содержит непустой заголовок. |
| 4 | `test_ad_has_content` | Попап содержит непустой текстовый контент. |
| 5 | `test_ad_close_button_works` | Нажатие на кнопку закрытия успешно скрывает попап. |
| 6 | `test_ad_can_be_reopened_by_reload` | После закрытия попапа перезагрузка страницы вызывает его повторное появление. |
| 7 | `test_ad_container_visible` | Контейнер рекламы корректно отображается в DOM. |
| 8 | `test_ad_close_button_visible` | Кнопка закрытия корректно отображается в DOM. |

#### Негативные сценарии (`TestAdsNegative`)

| № | Название теста | Описание |
|---|---|---|
| 1 | `test_ad_does_not_reopen_after_close` | После закрытия попап не появляется повторно в течение 5 секунд. |
| 2 | `test_ad_title_is_not_empty_string` | Заголовок рекламы не является пустой строкой. |
| 3 | `test_ad_close_button_not_clickable_after_close` | Попытка кликнуть по кнопке закрытия уже скрытого попапа вызывает исключение. |
| 4 | `test_ad_content_is_not_empty` | Контент рекламы не является пустой строкой. |

---

### 2. Страница "Calendar" (Календарь)

**Файлы:** `pages/calendar_page.py`, `tests/test_calendar.py`
**URL:** `https://practice-automation.com/calendars/`

#### Позитивные сценарии (`TestCalendarPositive`)

| № | Название теста | Описание |
|---|---|---|
| 1 | `test_page_loads_with_date_input` | Страница загружается с видимым полем ввода даты. |
| 2 | `test_click_opens_calendar` | Клик по инпуту открывает UI-календарь. |
| 3 | `test_set_date_via_input` | Ввод строки `"2025-06-15"` корректно сохраняется в атрибуте `value`. |
| 4 | `test_next_month_changes_label` | Клик по кнопке "Следующий месяц" меняет лейбл месяца. |
| 5 | `test_prev_month_returns_label` | Клик по "Предыдущий месяц" возвращает исходный лейбл. |
| 6 | `test_day_cells_are_present` | В открытом календаре отображается не менее 28 ячеек дней. |
| 7 | `test_click_day_updates_selection` | Клик по конкретному числу (15) обновляет значение в инпуте. |
| 8 | `test_submit_valid_date` | Ввод корректной даты и отправка формы показывают сообщение об успехе. |
| 9 | `test_format_hint_is_visible` | На странице видна подсказка с ожидаемым форматом даты. |

#### Негативные сценарии (`TestCalendarNegative`)

| № | Название теста | Описание |
|---|---|---|
| 1 | `test_calendar_hidden_before_click` | До клика по инпуту UI-календарь не отображается на экране. |
| 2 | `test_enter_letters_and_submit` | Ввод букв (`"abcd-ef-gh"`) и отправка формы вызывают ошибку валидации. |
| 3 | `test_submit_empty_date_shows_error` | Отправка формы с пустым полем даты обрабатывается. |
| 4 | `test_invalid_day_of_month_rejected` | Ввод несуществующей даты (`"2025-01-32"`) отклоняется с сообщением об ошибке. |
| 5 | `test_past_date_does_not_break_form` | Ввод даты из прошлого (`"1900-01-01"`) не ломает форму. |

---

### 3. Страница "Form Fields" (Поля формы)

**Файлы:** `pages/form_fields_page.py`, `tests/test_form_fields.py`
**URL:** `https://practice-automation.com/form-fields/`

#### Позитивные сценарии (`TestFormFieldsPositive`)

| № | Название теста | Описание |
|---|---|---|
| 1 | `test_automation_tools_list_has_5_items` | Список "Automation tools" содержит ровно 5 элементов и совпадает с ожидаемым. |
| 2 | `test_fill_message_with_automation_tools` | Текст из списка инструментов корректно извлекается, объединяется через запятую и вставляется в поле "Message". После отправки формы появляется алерт `"Message received!"`. |

---

### 4. Страница "Modals" (Модальные окна)

**Файлы:** `pages/modals_page.py`, `tests/test_modals.py`
**URL:** `https://practice-automation.com/modals/`

#### Позитивные сценарии (`TestModalsPositive`)

| № | Название теста | Описание |
|---|---|---|
| 1 | `test_simple_modal_opens` | Клик по кнопке открывает простое модальное окно. |
| 2 | `test_simple_modal_closes` | Повторный клик по крестику закрывает простое модальное окно. |
| 3 | `test_form_modal_opens` | Клик по соответствующей кнопке отображает форму внутри модального окна. |
| 4 | `test_form_fields_accept_input` | Поля `Name`, `Email`, `Message` успешно принимают и удерживают введенные значения. |
| 5 | `test_clear_form_resets_fields` | Метод очистки корректно сбрасывает значения всех полей формы в пустые строки. |
| 6 | `test_submit_valid_form_shows_success` | Заполнение валидными данными и отправка формы отображают сообщение `"Thank you for your response"`. |
| 7 | `test_submit_button_is_enabled` | Кнопка `Submit` в модальном окне активна по умолчанию. |
| 8 | `test_form_modal_close_button_works` | Кнопка закрытия корректно скрывает модальное окно с формой. |
| 9 | `test_long_message_is_accepted` | Поле `Message` успешно принимает и отображает длинное сообщение (500 символов). |

#### Негативные сценарии (`TestModalsNegative`)

| № | Название теста | Описание |
|---|---|---|
| 1 | `test_simple_modal_not_visible_before_click` | Простое модальное окно не отображается на экране до нажатия кнопки. |
| 2 | `test_form_modal_not_visible_before_click` | Модальное окно с формой не отображается на экране до нажатия кнопки. |
| 3 | `test_submit_empty_form_shows_error` | Попытка отправить пустую форму вызывает отображение ошибки. |
| 4 | `test_submit_without_required_name` | Отправка формы без заполнения поля `Name` вызывает ошибку валидации. |
| 5 | `test_submit_invalid_email_shows_error` | Ввод некорректного формата email вызывает ошибку валидации. |

---

## Пример отчёта о прохождении тестов

```bash
============================= test session starts ==============================
platform linux -- Python 3.10.12, pytest-7.4.0
plugins: selenium-4.10.0, allure-pytest-2.13.0
collected 34 items

tests/test_ads.py ............                                           [ 35%]
tests/test_calendar.py ..............                                    [ 76%]
tests/test_form_fields.py ..                                             [ 82%]
tests/test_modals.py ..............                                      [100%]

============================== 34 passed in 45.23s =============================
```
