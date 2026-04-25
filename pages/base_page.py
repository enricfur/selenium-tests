from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait: WebDriverWait[WebDriver] = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def input_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def has_text(self, locator, expected_text):
        return self.get_text(locator).strip() == expected_text

    def is_displayed(self, locator):
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except TimeoutException:
            return False

    def is_not_displayed(self, locator):
        return len(self.driver.find_elements(*locator)) == 0

    def get_alert_text(self):
        alert: Alert = self.wait.until(EC.alert_is_present())
        return alert.text

    def alert_has_text(self, expected_text):
        return self.get_alert_text().strip() == expected_text

    def accept_alert(self):
        alert: Alert = self.wait.until(EC.alert_is_present())
        alert.accept()
