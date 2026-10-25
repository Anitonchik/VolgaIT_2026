import pytest
import time
import allure
from pages.ads_page import AdsPage


@pytest.fixture
def page(driver):
    p = AdsPage(driver)
    p.load()
    return p


@allure.epic("UI Tests")
@allure.feature("Ads")
class TestAdsPositive:

    @allure.story("Page Load")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Страница Ads загружается с корректным заголовком")
    def test_page_loads_with_title(self, page):
        with allure.step("Получаем заголовок страницы"):
            title = page.get_page_title()
        with allure.step("Проверяем, что заголовок содержит 'Ads'"):
            assert "Ads" in title

    @allure.story("Ad Popup")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Рекламный попап автоматически появляется на странице")
    def test_ad_appears_automatically(self, page):
        with allure.step("Ожидаем появления рекламы до 15 секунд"):
            page.wait_for_ad(timeout=15)
        with allure.step("Проверяем, что реклама видна"):
            assert page.is_ad_visible()

    @allure.story("Ad Content")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Рекламный попап содержит непустой заголовок")
    def test_ad_has_title(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Получаем заголовок рекламы"):
            ad_title = page.get_ad_title()
        with allure.step("Проверяем, что заголовок не пустой"):
            assert ad_title.strip() != ""

    @allure.story("Ad Content")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Рекламный попап содержит непустой контент")
    def test_ad_has_content(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Получаем контент рекламы"):
            ad_content = page.get_ad_content()
        with allure.step("Проверяем, что контент не пустой"):
            assert ad_content.strip() != ""

    @allure.story("Ad Popup")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Кнопка закрытия успешно скрывает рекламный попап")
    def test_ad_close_button_works(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Закрываем рекламу"):
            page.close_ad()
        with allure.step("Ожидаем, что попап исчезнет"):
            page.wait_for_ad_closed()
        with allure.step("Проверяем, что реклама больше не видна"):
            assert not page.is_ad_visible()

    @allure.story("Ad Popup")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Перезагрузка страницы повторно открывает рекламный попап")
    def test_ad_can_be_reopened_by_reload(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Закрываем рекламу"):
            page.close_ad()
        with allure.step("Ожидаем закрытия попапа"):
            page.wait_for_ad_closed()
        with allure.step("Перезагружаем страницу"):
            page.load()
        with allure.step("Ожидаем повторного появления рекламы"):
            page.wait_for_ad(timeout=15)
        with allure.step("Проверяем, что реклама снова видна"):
            assert page.is_ad_visible()

    @allure.story("Ad UI Elements")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Контейнер рекламы отображается в DOM")
    def test_ad_container_visible(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Проверяем видимость контейнера"):
            assert page.is_visible(AdsPage.AD_CONTAINER)

    @allure.story("Ad UI Elements")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Кнопка закрытия рекламы отображается в DOM")
    def test_ad_close_button_visible(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Проверяем видимость кнопки закрытия"):
            assert page.is_visible(AdsPage.AD_CLOSE_BTN)


@allure.epic("UI Tests")
@allure.feature("Ads")
class TestAdsNegative:

    @allure.story("Ad Popup")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("После закрытия попап не открывается повторно")
    def test_ad_does_not_reopen_after_close(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Закрываем рекламу"):
            page.close_ad()
        with allure.step("Ожидаем закрытия попапа"):
            page.wait_for_ad_closed()
        with allure.step("Ждём 5 секунд"):
            time.sleep(5)
        with allure.step("Проверяем, что реклама не появилась снова"):
            assert not page.is_ad_visible()

    @allure.story("Ad Content")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Заголовок рекламы не является пустой строкой")
    def test_ad_title_is_not_empty_string(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Получаем заголовок"):
            title = page.get_ad_title()
        with allure.step("Проверяем, что это не пустая строка"):
            assert title.strip() != ""

    @allure.story("Ad Popup")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Кнопка закрытия недоступна после закрытия попапа")
    def test_ad_close_button_not_clickable_after_close(self, page):
        from selenium.common.exceptions import TimeoutException
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Закрываем рекламу"):
            page.close_ad()
        with allure.step("Ожидаем закрытия попапа"):
            page.wait_for_ad_closed()
        with allure.step("Пытаемся кликнуть по кнопке закрытия и ожидаем исключение"):
            with pytest.raises((TimeoutException, Exception)):
                page.click(AdsPage.AD_CLOSE_BTN)

    @allure.story("Ad Content")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("Контент рекламы не является пустым")
    def test_ad_content_is_not_empty(self, page):
        with allure.step("Ожидаем появления рекламы"):
            page.wait_for_ad()
        with allure.step("Получаем контент"):
            content = page.get_ad_content()
        with allure.step("Проверяем, что контент не пустой"):
            assert content.strip() != ""