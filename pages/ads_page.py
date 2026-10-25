# pages/ads_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AdsPage(BasePage):
    URL = "https://practice-automation.com/ads/"

    AD_OVERLAY = (By.ID, "pum-1272")
    AD_CONTAINER = (By.CSS_SELECTOR, "#pum-1272 .pum-container")
    AD_TITLE = (By.ID, "pum_popup_title_1272")
    AD_CONTENT = (By.CSS_SELECTOR, "#pum-1272 .pum-content p")
    AD_CLOSE_BTN = (By.CSS_SELECTOR, "#pum-1272 .pum-close")

    PAGE_TITLE = (By.CSS_SELECTOR, "h1[itemprop='headline']")

    def load(self):
        self.open(self.URL)

    def wait_for_ad(self, timeout=15):
        return self.wait_for_visible(self.AD_OVERLAY, timeout=timeout)

    def is_ad_visible(self) -> bool:
        try:
            overlay = self.driver.find_element(*self.AD_OVERLAY)
            return overlay.is_displayed() and "pum-active" in (overlay.get_attribute("class") or "")
        except Exception:
            return False

    def get_ad_title(self) -> str:
        return self.get_text(self.AD_TITLE)

    def get_ad_content(self) -> str:
        return self.get_text(self.AD_CONTENT)

    def close_ad(self):
        self.click(self.AD_CLOSE_BTN)

    def wait_for_ad_closed(self, timeout=10):
        return self.wait.until(
            lambda d: "pum-active" not in (d.find_element(*self.AD_OVERLAY).get_attribute("class") or ""),
            message="Рекламный попап не закрылся",
        )

    def get_page_title(self) -> str:
        return self.get_text(self.PAGE_TITLE)