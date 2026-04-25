from selenium.webdriver.common.by import By

class FBankLocators:
    RUB_ACCOUNT = (By.XPATH, "//div[@role = 'button'][1]")
    CARD_INPUT = (By.XPATH, "//input")
    INPUT_TRANSFER_SUM = (By.XPATH, "(//div)[11]//input[2]")
    TRANSFER_BUTTON = (By.XPATH, "//button")
    NOT_ENOUGH_MONEY_LABEL = (By.XPATH, "(//div)[11]//span[2]")
    COMMISSION = (By.XPATH, "(//p//span)[7]")
