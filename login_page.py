from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class LoginPage:
    """Класс для страницы логина"""
    def __init__(self, driver):
        """Локаторы"""
        self.driver = driver
        self.url = "https://www.saucedemo.com/"
        self.username_field = (By.CSS_SELECTOR, '#user-name')
        self.password_field = (By.CSS_SELECTOR, '#password')
        self.login_button = (By.CSS_SELECTOR, 'input[name="login-button"]')

    def open(self):
        """Открытие страницы логина"""
        self.driver.get(self.url)

    def enter_username(self, username: str):
        """Ввод имени пользователя"""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.username_field)).send_keys(username)

    def enter_password(self, password: str):
        """Ввод пароля пользователя"""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.password_field)).send_keys(password)

    def click_login(self):
        """Нажатие кнопки логина"""
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.login_button)).click()

    def login(self, username: str, password: str):
        """Выполнение полного процесса логина"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()