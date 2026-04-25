from config.config import Config
from pages.base_page import BasePage
from utils.locators import FBankLocators


class FBankPage(BasePage):
    """Главная страница приложения."""

    URL = Config.BASE_URL

    def open_page(self):
        self.open(self.URL)
        return self

    def enter_card_number(self, card_number):
        self.input_text(FBankLocators.CARD_INPUT, card_number)
        return self

    def enter_transfer_sum(self, amount):
        self.input_text(FBankLocators.INPUT_TRANSFER_SUM, amount)
        return self

    def click_rub_account(self):
        self.click(FBankLocators.RUB_ACCOUNT)
        return self

    def create_transfer(self):
        self.click(FBankLocators.TRANSFER_BUTTON)
        return self
