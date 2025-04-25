from selenium import webdriver
from login_page import LoginPage
from inventory_page import InventoryPage
from cart_page import CartPage
from checkout_page import CheckoutPage


def get_driver():
    """Создает и возвращает веб-драйвер с настройками"""
    options: webdriver.ChromeOptions = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--incognito")
    return webdriver.Chrome(options=options)

def main():
    driver = get_driver()
    try:
        # Инициализация страниц
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)

        # 1. Авторизация
        login_page.open()
        print("Страница загружена: ", driver.current_url)
        login_page.login("standard_user", "secret_sauce")

        # 2. Проверка товара
        products = inventory_page.get_products()
        print(f"Найдено товаров: {len(products)}")
        assert len(products) == 6, f"Ожидалось 6 товаров, но найдено: {len(products)}"

        for index, product in enumerate(inventory_page.get_product_details(), 1):
            print(f"\nТовар {index}:")
            print(f"Заголовок: {product['title']}")
            print(f"Описание: {product['description']}")
            print(f"Цена: {product['price']}")

        # 3. Сортировка по цене
        inventory_page.sort_by_price_low_to_high()
        prices = inventory_page.get_prices()
        sorted_prices = sorted(prices)
        if prices == sorted_prices:
            print(f"Товары отсортированы по возрастанию цены:\n{prices}\n")
        else:
            print("Товары не отсортированы правильно.")
            print(f"Получено: {prices}\n")
            print(f"Ожидалось: {sorted_prices}\n")

        # 4. Добавление случайного товара в корзину
        random_product = inventory_page.add_random_product_to_cart()
        if inventory_page.is_remove_button_displayed(random_product):
            print("Кнопка изменилась на 'Remove\n")
        else:
            print("Кнопка не изменилась!")

        # Проверка количества товаров в корзине
        cart_count = inventory_page.get_cart_item_count()
        assert cart_count > 0, "Значок корзины не отображает количество добавленных товаров"
        print(f"✅ Тест пройден: В корзине отображается {cart_count} товар(а/ов)")

        # 5. Переход в корзину и оформление заказа
        inventory_page.go_to_cart()
        cart_items = cart_page.get_cart_items()
        if cart_items:
            for item in cart_items:
                print(f"Добавленный товар отображается - {item['name']}\n")
        else:
            print("Корзина пуста\n")

        cart_page.go_to_checkout()
        checkout_page.fill_checkout_form("Denis", "Pavroz", "228")
        checkout_page.finish_checkout()
        checkout_page.back_to_home()
        print("Покупка завершена!\nВыполнен переход на главную страницу!")

    finally:
        input("Нажмите Enter, чтобы закрыть...")
        driver.quit()

if __name__ == "__main__":
    main()



