import selenium
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class User:

    url = 'https://anymoney.e-cash.pro/'

    def __init__(self, user=None):
        if user:
            self.email = user['email']
            self.pwd = user['pwd']
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)

    def authorization(self, email, pwd):
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header__logout-button')))
        self.driver.find_element_by_class_name('header__logout-button').click()
        self.wait.until(EC.presence_of_element_located((By.ID, 'login')))
        self.driver.find_element_by_id('login').send_keys(email)
        self.driver.find_element_by_id('password').send_keys(pwd)
        self.driver.find_element_by_class_name('auth-modal__button-authorization').click()
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header__link--login')))
        except TimeoutException:
            print('Error! NO LOGIN!')

    def logout(self):
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'header__logout-button')))
        b = self.driver.find_element_by_class_name('header__logout-button')
        b.click()
        sleep(2)


