from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.test.utils import override_settings
from time import sleep

@override_settings(DEBUG=True)
class test_main_functions(LiveServerTestCase):
    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
    
    def testLoginUser(self):
        user = User.objects.create_user(username='user', password='user')
        self.driver.get(self.live_server_url + "/users/login")
        
        # Username
        usernameInput = self.driver.find_element("id", "id_username")
        usernameInput.send_keys("user")
        
        # Password
        passwordInput = self.driver.find_element("id", "id_password")
        passwordInput.send_keys("user")
        
        # Submit button
        submitButton = self.driver.find_elements(By.TAG_NAME, "button")[0]
        submitButton.click()
        
        self.assertEquals(self.driver.current_url, self.live_server_url + "/app")
    
    def testRegisterUser_BotError(self):
        self.driver.get(self.live_server_url + "/users/register")
        
        # Username
        usernameInput = self.driver.find_element("id", "id_username")
        usernameInput.send_keys("user2")
        
        # Email
        emailInput = self.driver.find_element("id", "id_email")
        emailInput.send_keys("test.test@test.com")
        
        # Password
        passwordInput = self.driver.find_element("id", "id_password1")
        passwordInput.send_keys("User2User2")
        
        # Password Confirm
        passwordInput = self.driver.find_element("id", "id_password2")
        passwordInput.send_keys("User2User2")
        
        submitButton = self.driver.find_elements(By.TAG_NAME, "button")[0]
        submitButton.click()
        
        sleep(0.5)
        
        alert = self.driver.find_elements(By.TAG_NAME, "div")[0]
        self.assertEquals(alert.text, "reCaptcha Überprüfung fehlgeschlagen. Versuche es bitte erneut.")
