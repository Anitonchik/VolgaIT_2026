from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CalendarPage(BasePage):
    URL = "https://practice-automation.com/calendars/"

    DATE_INPUT = (By.ID, "g1065-1-selectorenteradate")
    FORMAT_HINT = (By.ID, "g1065-1-selectorenteradate-text-format")
    FIELD_ERROR_MSG = (By.ID, "g1065-1-selectorenteradate-text-error-message")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    SUCCESS_MESSAGE = (By.XPATH, "//h4[contains(text(), 'Thank you for your response')]")

    CALENDAR_CONTAINER = (By.CSS_SELECTOR, "div.dp-below")
    MONTH_BUTTON = (By.CSS_SELECTOR, "div.dp-below .dp-cal-month")
    NEXT_BUTTON = (By.CSS_SELECTOR, "div.dp-below .dp-next")
    PREV_BUTTON = (By.CSS_SELECTOR, "div.dp-below .dp-prev")
    DAYS = (By.CSS_SELECTOR, "div.dp-below .dp-day")

    def load(self):
        self.open(self.URL)

    def open_calendar(self):
        self.click(self.DATE_INPUT)
        self.wait.until(EC.visibility_of_element_located(self.CALENDAR_CONTAINER))

    def is_calendar_visible(self) -> bool:
        return self.is_visible(self.CALENDAR_CONTAINER)

    def type_date(self, date_str: str):
        self.type_text(self.DATE_INPUT, date_str)

    def get_input_value(self) -> str:
        return self.find(self.DATE_INPUT).get_attribute("value")

    def blur_field(self):
        self.driver.find_element(By.TAG_NAME, "body").click()

    def get_month_label(self) -> str:
        return self.get_text(self.MONTH_BUTTON)

    def click_next_month(self):
        self.click(self.NEXT_BUTTON)

    def click_prev_month(self):
        self.click(self.PREV_BUTTON)

    def get_days(self):
        return self.find_all(self.DAYS)

    def click_day_by_number(self, day: int):
        locator = (
            By.XPATH,
            "//div[contains(@class,'dp-below')]"
            "//button[contains(@class,'dp-day') and not(contains(@class,'dp-edge-day'))"
            f" and normalize-space()='{day}']"
        )
        self.click(locator)

    def submit(self):
        self.click(self.SUBMIT_BUTTON)

    def is_success_message_visible(self) -> bool:
        return self.is_visible(self.SUCCESS_MESSAGE)

    def get_field_error_text(self) -> str:
        return self.get_text(self.FIELD_ERROR_MSG)

    def wait_for_success(self):
        self.wait_for_visible(self.SUCCESS_MESSAGE, timeout=15)
        return True