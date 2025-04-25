from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
import random


class InventoryPage:
    """Класс для страницы с товарами"""
    def __init__(self, driver: WebDriver):
        """Локаторы"""
        self.driver = driver
        self.product_items = (By.CSS_SELECTOR, ".inventory_item") # Карточки продуктов
        self.product_name = (By.CSS_SELECTOR, ".inventory_item_name") # Название продукта
        self.product_description = (By.CSS_SELECTOR, ".inventory_item_desc") # Описание продукта
        self.product_price = (By.CSS_SELECTOR, ".inventory_item_price") # Цена продукта
        self.sort_dropdown = (By.CSS_SELECTOR, ".product_sort_container") # Кнопка сортировки
        self.sort_lohi_option = (By.CSS_SELECTOR, "option[value='lohi']") # Необходимая сортировка
        self.add_to_cart_button = (By.CSS_SELECTOR, "button.btn_primary") # Кнопка добавления продукта
        self.remove_button = (By.CSS_SELECTOR, "button.btn_secondary") # Проверка, что кнопка изменилась на "Remove"
        self.cart_link = (By.CSS_SELECTOR, ".shopping_cart_link") # Кнопка корзины
        self.cart_badge = (By.CSS_SELECTOR, ".shopping_cart_badge") # Отображение сколько товаров в корзине


    def get_products(self) -> List[WebElement]:
        """Возвращает список товаров на странице"""
        return WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(self.product_items))

    def get_product_details(self) -> list[dict[str, str]]:
        """Возвращает список словарей с информацией о товарах"""
        products = self.get_products()
        details = []
        for product in products:
            details.append({
                "title": product.find_element(*self.product_name).text,
                "description": product.find_element(*self.product_description).text,
                "price": product.find_element(*self.product_price).text
            })
        return details

    def sort_by_price_low_to_high(self):
        """Сортирует товары по цене от низкой к высокой"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.sort_dropdown)).click()
        WebDriverWait(self.driver, 10). until(EC.element_to_be_clickable(self.sort_lohi_option)).click()

    def get_prices(self) -> List[float]:
        """Возвращает отсортированный список цен товаров"""
        price_elements = WebDriverWait(self.driver, 10).until(EC.visibility_of_all_elements_located(self.product_price))
        return [float(price.text.replace('$', '')) for price in price_elements]

    def add_random_product_to_cart(self):
        """Добавляет случайный товар в корзину и возвращает элемент товара"""
        products = self.get_products()
        random_product = random.choice(products)
        random_product.find_element(*self.add_to_cart_button).click()
        return random_product

    def is_remove_button_displayed(self, product: WebElement) -> bool:
        """Проверяет, что кнопка "Remove" отображается у добавленного товара"""
        return product.find_element(*self.remove_button).text.strip().lower() == "remove"

    def get_cart_item_count(self) -> int:
        """Возвращает количество товаров в корзине"""
        badge = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.cart_badge))
        return int(badge.text)

    def go_to_cart(self):
        """Переходит в корзину"""
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.cart_link)).click()









