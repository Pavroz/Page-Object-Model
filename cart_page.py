from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Класс для страницы корзины"""
    def __init__(self, driver: WebDriver):
        """Локаторы"""
        self.driver = driver
        self.cart_item = (By.CSS_SELECTOR, '.cart_item')
        self.product_name = (By.CSS_SELECTOR, '.inventory_item_name')
        self.checkout_button = (By.CSS_SELECTOR, '#checkout')

    def get_cart_items(self) -> list[dict]:
        """Возвращает список товаров в корзине"""
        items = WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located(self.cart_item))
        return [{"name": item.find_element(*self.product_name).text} for item in items]

    def go_to_checkout(self):
        """Переходит к оформлению заказа"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.checkout_button)).click()