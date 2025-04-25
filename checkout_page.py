from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


class CheckoutPage:
    """Класс для страницы оформления заказа"""
    def __init__(self, driver: WebDriver):
        """Локаторы"""
        self.driver = driver
        self.first_name_field = (By.CSS_SELECTOR, '[data-test="firstName"]')
        self.last_name_field = (By.CSS_SELECTOR, '[placeholder="Last Name"]')
        self.postal_code_field = (By.CSS_SELECTOR, '#postal-code')
        self.continue_button = (By.ID, 'continue')
        self.finish_button = (By.ID, 'finish')
        self.back_home_button = (By.CSS_SELECTOR, 'button[name="back-to-products"]')

    def fill_checkout_form(self, first_name: str, last_name: str, postal_code: str):
        """Заполяет форму оформления заказа"""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.first_name_field)).send_keys(first_name)
        self.driver.find_element(*self.last_name_field).send_keys(last_name)
        self.driver.find_element(*self.postal_code_field).send_keys(postal_code)
        self.driver.find_element(*self.continue_button).click()

    def finish_checkout(self):
        """Завершает покупку"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.finish_button)).click()

    def back_to_home(self):
        """Возвращается на главную страницу"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.back_home_button)).click()