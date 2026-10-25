import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    # options.add_argument("--headless")
    drv = webdriver.Chrome(options=options)
    drv.implicitly_wait(5)
    yield drv
    drv.quit()

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