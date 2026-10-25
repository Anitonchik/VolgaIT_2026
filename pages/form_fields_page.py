from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    URL = "https://practice-automation.com/form-fields/"

    NAME_INPUT = (By.ID, "name-input")
    EMAIL_INPUT = (By.ID, "email")
    MESSAGE_INPUT = (By.ID, "message")
    SUBMIT_BTN = (By.ID, "submit-btn")

    AUTOMATION_TOOLS_LIST = (
        By.XPATH,
        "//label[contains(normalize-space(.), 'Automation tools')]/following-sibling::ul[1]/li",
    )

    def load(self):
        self.open(self.URL)

    def fill_name(self, name):
        self.type_text(self.NAME_INPUT, name)

    def fill_email(self, email):
        self.type_text(self.EMAIL_INPUT, email)

    def fill_message(self, message):
        self.type_text(self.MESSAGE_INPUT, message)

    def get_message_value(self) -> str:
        return self.find(self.MESSAGE_INPUT).get_attribute("value")

    def get_automation_tools_list(self) -> list[str]:
        elements = self.find_all(self.AUTOMATION_TOOLS_LIST)
        return [el.text.strip() for el in elements if el.text.strip()]

    def get_automation_tools_text(self) -> str:
        return ", ".join(self.get_automation_tools_list())

    def submit(self):
        button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BTN))
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", button
        )
        try:
            button.click()
        except ElementClickInterceptedException:
            self.driver.execute_script("arguments[0].click();", button)