
from pprint import pprint
import random
from typing import List

import undetected_chromedriver as uc
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

# Константы
WEB_DRIVER_OPTIONS = ["--start-maximized", "--incognito"] # Список опций
URL = "https://www.saucedemo.com/"
USERNAMES = ["standard_user",
"locked_out_user",
"problem_user",
"performance_glitch_user",
"error_user",
"visual_user"]

def get_driver(driver_options: list = WEB_DRIVER_OPTIONS) -> webdriver.Chrome:
    """
    Создание драйвера с настройками
    :return: webdriver.Chrome
    """
    # Если drive_options не пустой, то создается объект webdriver.ChromeOptions() для настройки браузера
    options: webdriver.ChromeOptions = webdriver.ChromeOptions()
    if driver_options:
        for option in driver_options:
            options.add_argument(option)
        return webdriver.Chrome(options=options) # Если опции есть, в драйвер добавляется аргумент
    else:
        return webdriver.Chrome() # Если опций нет, то возвращается драйвер без настроек


def get_uc_driver(driver_settings: list,) -> webdriver.Chrome:

    options = uc.ChromeOptions()

    for option in driver_settings:
        options.add_argument(option)

    driver = uc.Chrome(options=options)
    return driver


# Открытие страница
def get_page(url: str, driver: webdriver.Chrome) -> None:
    driver.get(url)


# Авторизация
def auth(login: str, password: str, driver: webdriver) -> None:
    """
    Авторизация
    :param login: логин пользователя
    :param password: пароль пользователя
    :param driver: webdriver
    :return: None
    """
    input_login: WebElement = driver.find_element(By.CSS_SELECTOR, '#user-name')
    input_login.send_keys(login)
    time.sleep(1)

    input_password: WebElement = driver.find_element(By.CSS_SELECTOR, '#password')
    input_password.send_keys(password)
    time.sleep(1)

    input_auth: WebElement = driver.find_element(By.CSS_SELECTOR, 'input[name="login-button"]')
    input_auth.click()
    time.sleep(2)


def main():
    driver: webdriver.Chrome = get_driver()
    # driver: webdriver.Chrome = get_uc_driver(driver_settings=WEB_DRIVER_OPTIONS)
    get_page(URL, driver)
    print("Страница загружена: ", driver.current_url)
    time.sleep(1)

    # 1. Авторизация
    # Под конкретным юзером
    auth(login = "standard_user", password = "secret_sauce", driver = driver)

    # Выбираем случайный логин из списка USERNAMES и авторизуемся
    # login = random.choice(USERNAMES)  # Выбираем случайный логин
    # print(f"Авторизация для {login}...")
    # auth(login=login, password="secret_sauce", driver=driver)


    # 2. Проверка количества товаров на странице (должно быть 6) и вывод названия, описания и цену каждого товара
    search_products: List[WebElement] = driver.find_elements(By.CSS_SELECTOR, '.inventory_item')
    print(f"Найдено товаров: {len(search_products)}")
    # assert - проверка утверждения, если True, то код продолжается, а если False, то выполняется код после запятой
    assert len(search_products) == 6, f"Ожидалось 6 товаров, но найдено: {len(search_products)}"

    for index, product in enumerate(search_products, 1):
        title = product.find_element(By.CSS_SELECTOR, '.inventory_item_name ').text
        description = product.find_element(By.CSS_SELECTOR, '.inventory_item_desc').text
        price = product.find_element(By.CSS_SELECTOR, '.inventory_item_price').text

        print(f"\nТовар {index}:")
        print(f"Заголовок: {title}")
        print(f"Описание: {description}")
        print(f"Цена: {price}")
        print()


    # 3. Фильтрация товаров
    # 3.1. Выбрать сортировку "Price (low to high)"
    input_filter = driver.find_element(By.CSS_SELECTOR, '.product_sort_container')
    input_filter.find_element(By.CSS_SELECTOR, 'option[value="lohi"]').click()

    # 3.2. Проверить, что товары отсортированы по возрастанию цены
    price_elements = driver.find_elements(By.CSS_SELECTOR, '.inventory_item_price')
    prices = [float(price.text.replace('$', '')) for price in price_elements]
    sorted_prices = sorted(prices)
    if prices == sorted_prices:
        print(f"Товары отсортированы по возрастанию цены: \n"
              f"{prices}\n")
    else:
        print("Товары не отсортированы правильно.")
        print(f"Получено: {prices}")
        print(f"Ожидалось: {sorted_prices}")



    # 4. Добавление товара в корзину
    # 4.1. Добавить конкретный товар в корзину
    # add_product = driver.find_element(By.CSS_SELECTOR, 'button[name="add-to-cart-sauce-labs-bike-light"]')
    # add_product.click()
    # time.sleep(1)
    # Добавить случайный товар в корзину
    # Сбор всех карточек на странице
    products_list = driver.find_elements(By.CSS_SELECTOR, 'div[class="inventory_item"]')
    # Создание переменной, в которую помещается рандомная карточка
    random_product = random.choice(products_list)
    print(f"Выбран продукт: {random_product.text}")
    # Нажатие на рандомную карточку
    click_on_random_product: WebElement = random_product.find_element(By.CSS_SELECTOR, 'button.btn_primary')
    click_on_random_product.click()
    time.sleep(5)

    # 4.2. Проверить, что кнопка изменилась на "Remove"
    remove_button = random_product.find_element(By.CLASS_NAME, 'btn_secondary')
    if remove_button and remove_button.text.strip().lower() == "remove":
        print(f"Кнопка изменилась на 'Remove'\n")
    else:
        print(f"Кнопка не изменилась!\n")

    # 4.3. Убедиться, что иконка корзины показывает количество товаров
    try:
        cart_icon = driver.find_element(By.CSS_SELECTOR, '.shopping_cart_link')
        cart_badge = driver.find_element(By.CSS_SELECTOR, '.shopping_cart_badge')
        cart_count = cart_badge.text

        # Вариант ниже через assert
        # if cart_count.isdigit() and int(cart_count) > 0:
        #     print(f"Корзина не пуста! В ней {cart_count} товар(а/ов).")
        # else:
        #     print("Корзина пуста или не удалось определить количество товар(а/ов).")

        # Вариант вместо кода выше, где if-else
        assert cart_count.isdigit(), "Значок корзины не содержит цифру"
        assert int(cart_count) > 0, "Значок корзины не отображает количество добавленных товаров"
        print(f"\n✅ Тест пройден: В корзине отображается {cart_count} товар(а/ов)")

    except NoSuchElementException:
        print("Не удалось найти элемент корзины или бейджик количества.")

    # 5. Переход в корзину и оформление заказа
    # 5.1. Перейти в корзину
    click_on_basket = driver.find_element(By.CSS_SELECTOR, '.shopping_cart_link')
    click_on_basket.click()

    # 5.2. Проверить, что товар отображается
    check_products = driver.find_elements(By.CSS_SELECTOR, '.cart_item')
    name_products = driver.find_elements(By.CSS_SELECTOR, '#item_0_title_link')
    if len(check_products) > 0:
        for product in name_products:
            product_name = product.text
            product_href = product.get_attribute('href')
            print(f"Добавленный товар отображается - {product_name}\n"
                  f"Ссылка на товар - {product_href}")
    else:
        print("Корзина пуста")

    # 5.3. Нажать Checkout
    click_on_checkout = driver.find_element(By.CSS_SELECTOR, "#checkout")
    click_on_checkout.click()

    # 5.4. Заполнить форму (First Name, Last Name, Postal Code)
    input_firstname = driver.find_element(By.CSS_SELECTOR, '[data-test="firstName"]')
    input_firstname.send_keys("Denis")
    input_lastname = driver.find_element(By.CSS_SELECTOR, '[placeholder="Last Name"]')
    input_lastname.send_keys("Pavroz")
    input_postalcode = driver.find_element(By.CSS_SELECTOR, '#postal-code')
    input_postalcode.send_keys("228")
    time.sleep(10)
    driver.find_element(By.ID, 'continue').send_keys(Keys.ENTER)

    # 5.5. Завершить покупку
    finish_input: WebElement = driver.find_element(By.ID, 'finish')
    finish_input.click()
    time.sleep(2)
    back_home_input: WebElement = driver.find_element(By.CSS_SELECTOR, 'button[name="back-to-products"]')
    back_home_input.click()
    print("Покупка завершена!\n"
          "Выполнен переход на главную страницу!")

    print()
    input("Нажмите Enter, чтобы закрыть...")
    driver.quit()

main()







