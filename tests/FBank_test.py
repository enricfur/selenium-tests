import allure

from pages.FBank_page import FBankPage
from utils.locators import FBankLocators


def _precondition(driver):
    page = FBankPage(driver).open_page()

    with allure.step("Выбрать рублевый счет"):
        page.click_rub_account()
        assert page.is_displayed(FBankLocators.CARD_INPUT)

    return page


class TestFBank:

    @allure.title("Создание перевода с картой с 15 символами")
    def test_transfer_card_with_15_symbols(self, driver):
        with allure.step("Открыть страницу"):
            page = _precondition(driver)

        with allure.step("Ввести в поле номер карты с 15 символами"):
            page.enter_card_number("123456789012345")
            assert page.is_not_displayed(FBankLocators.INPUT_TRANSFER_SUM)

    @allure.title("Создание перевода с картой с 16 символами и суммой больше доступной")
    def test_transfer_card_with_16_symbols(self, driver):
        with allure.step("Открыть страницу"):
            page = _precondition(driver)

        with allure.step("Ввести в поле номер карты с 16 символами"):
            page.enter_card_number("1234567890123456")
            assert page.is_displayed(FBankLocators.INPUT_TRANSFER_SUM)
            assert page.is_displayed(FBankLocators.TRANSFER_BUTTON)

        with allure.step("В поле суммы перевода ввести 100000"):
            page.enter_transfer_sum("100000")
            assert page.is_not_displayed(FBankLocators.TRANSFER_BUTTON)
            assert page.has_text(
                FBankLocators.NOT_ENOUGH_MONEY_LABEL,
                "Недостаточно средств на счете",
            )

    @allure.title("Создание перевода с картой с 17 символами")
    def test_transfer_card_with_17_symbols(self, driver):
        with allure.step("Открыть страницу"):
            page = _precondition(driver)

        with allure.step("Ввести в поле номер карты с 17 символами"):
            page.enter_card_number("12345678901234567")
            assert page.is_not_displayed(FBankLocators.INPUT_TRANSFER_SUM)

    @allure.title("Расчет комиссии для суммы 10 рублей")
    def test_transfer_with_10_rub(self, driver):
        with allure.step("Открыть страницу"):
            page = _precondition(driver)

        with allure.step("Ввести в поле номер карты с 16 символами"):
            page.enter_card_number("1234567890123456")
            assert page.is_displayed(FBankLocators.INPUT_TRANSFER_SUM)
            assert page.is_displayed(FBankLocators.TRANSFER_BUTTON)

        with allure.step("В поле суммы перевода ввести 10"):
            page.enter_transfer_sum("10")
            assert page.is_displayed(FBankLocators.TRANSFER_BUTTON)
            assert page.has_text(FBankLocators.COMMISSION, "1")

    @allure.title("Расчет комиссии для суммы 100 рублей и отправка перевода")
    def test_with_100_rub_transfer(self, driver):
        with allure.step("Открыть страницу"):
            page = _precondition(driver)

        with allure.step("Ввести в поле номер карты с 16 символами"):
            page.enter_card_number("1234567890123456")
            assert page.is_displayed(FBankLocators.INPUT_TRANSFER_SUM)
            assert page.is_displayed(FBankLocators.TRANSFER_BUTTON)

        with allure.step("В поле суммы перевода ввести 100"):
            page.enter_transfer_sum("100")
            assert page.is_displayed(FBankLocators.TRANSFER_BUTTON)
            assert page.has_text(FBankLocators.COMMISSION, "10")

        with allure.step("Нажать кнопку перевода"):
            page.create_transfer()
            assert page.alert_has_text("Перевод 100 ₽ на карту 1234567890123456 принят банком!")
            page.accept_alert()
            assert page.has_text(FBankLocators.RUB_RESERVED, "1'300")

