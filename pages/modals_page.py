# pages/modals_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ModalsPage(BasePage):
    URL = "https://practice-automation.com/modals/"

    SIMPLE_MODAL_BTN = (By.ID, "simpleModal")
    FORM_MODAL_BTN = (By.ID, "formModal")

    SIMPLE_MODAL_CONTAINER = (By.ID, "pum-1318")
    SIMPLE_MODAL_CLOSE = (By.CSS_SELECTOR, "#pum-1318 .pum-close")

    FORM_MODAL_CONTAINER = (By.ID, "pum-674")
    NAME_INPUT = (By.ID, "g1051-name")
    EMAIL_INPUT = (By.ID, "g1051-email")
    MESSAGE_INPUT = (By.ID, "contact-form-comment-g1051-message")
    SUBMIT_BTN = (By.CSS_SELECTOR, "#pum-674 button[type='submit']")
    SUCCESS_MESSAGE = (By.XPATH, "//h4[contains(text(), 'Thank you for your response')]")
    FORM_ERROR = (By.CSS_SELECTOR, "#pum-674 .contact-form__error-message")
    NAME_ERROR = (By.ID, "g1051-name-text-error-message")
    EMAIL_ERROR = (By.ID, "g1051-email-email-error-message")
    FORM_MODAL_CLOSE = (By.CSS_SELECTOR, "#pum-674 .pum-close")
    FORM_SUBMIT_BTN_EL = (By.CSS_SELECTOR, "#pum-674 button[type='submit']")

    AUTOMATION_TOOLS_LIST = (
        By.XPATH,
        "//h2[contains(text(), 'Automation Tools')]/following-sibling::ul/li"
        " | //h3[contains(text(), 'Automation Tools')]/following-sibling::ul/li",
    )

    def load(self):
        self.open(self.URL)

    def open_simple_modal(self):
        self.click(self.SIMPLE_MODAL_BTN)
        self.wait.until(EC.visibility_of_element_located(self.SIMPLE_MODAL_CONTAINER))

    def is_simple_modal_visible(self) -> bool:
        return self.is_visible(self.SIMPLE_MODAL_CONTAINER)

    def close_simple_modal(self):
        self.click(self.SIMPLE_MODAL_CLOSE)
        self.wait.until(EC.invisibility_of_element_located(self.SIMPLE_MODAL_CONTAINER))

    def open_form_modal(self):
        self.click(self.FORM_MODAL_BTN)
        self.wait.until(EC.visibility_of_element_located(self.FORM_MODAL_CONTAINER))

    def is_form_modal_visible(self) -> bool:
        return self.is_visible(self.FORM_MODAL_CONTAINER)

    def close_form_modal(self):
        self.click(self.FORM_MODAL_CLOSE)
        self.wait.until(EC.invisibility_of_element_located(self.FORM_MODAL_CONTAINER))

    def get_input_value(self, locator) -> str:
        return self.find(locator).get_attribute("value")

    def get_automation_tools_text(self) -> str:
        elements = self.find_all(self.AUTOMATION_TOOLS_LIST)
        tools = [el.text.strip() for el in elements if el.text.strip()]
        return ", ".join(tools)

    def fill_form(self, name="", email="", message=""):
        if name:
            self.type_text(self.NAME_INPUT, name)
        if email:
            self.type_text(self.EMAIL_INPUT, email)
        if message:
            self.type_text(self.MESSAGE_INPUT, message)

    def clear_form(self):
        for loc in (self.NAME_INPUT, self.EMAIL_INPUT, self.MESSAGE_INPUT):
            self.find(loc).clear()

    def submit_form(self):
        self.click(self.SUBMIT_BTN)

    def is_success_visible(self) -> bool:
        return self.is_visible(self.SUCCESS_MESSAGE)

    def is_form_error_visible(self) -> bool:
        return self.is_visible(self.FORM_ERROR)

    def get_name_error_text(self) -> str:
        return self.get_text(self.NAME_ERROR)

    def get_email_error_text(self) -> str:
        return self.get_text(self.EMAIL_ERROR)

    def is_submit_button_enabled(self) -> bool:
        return self.find(self.FORM_SUBMIT_BTN_EL).is_enabled()