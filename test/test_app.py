import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class FlaskAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()  
        cls.driver.get("http://127.0.0.1:5000")
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def wait_for_element(self, by, value, timeout=20):
        driver = self.driver
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            raise e

    def wait_for_element_to_be_clickable(self, by, value, timeout=20):
        driver = self.driver
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            return element
        except Exception as e:

            raise e

    def test_1_register(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/register")

        try:


            username_field = self.wait_for_element(By.ID, "username")
            print("Found username field:", username_field)
            email_field = self.wait_for_element(By.ID, "email")
            password_field = self.wait_for_element(By.ID, "password")
            confirm_password_field = self.wait_for_element(By.ID, "confirm_password")
            submit_button = self.wait_for_element_to_be_clickable(By.ID, "register_btn")
            print("Found register button:", submit_button)

            username_field.send_keys("testuser000")
            email_field.send_keys("testuser000@example.com")
            password_field.send_keys("testpassword")
            confirm_password_field.send_keys("testpassword")
            submit_button.click()


            success_message = self.wait_for_element(By.XPATH, "//div[contains(text(), 'Registration Successful!')]")
            self.assertIn("Registration Successful!", success_message.text)
        except Exception as e:
            print("Error in test_1_register")
            print("Exception message:", str(e))

            raise e

    def test_2_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")

        try:


            username_field = self.wait_for_element(By.ID, "username")
            password_field = self.wait_for_element(By.ID, "password")
            submit_button = self.wait_for_element_to_be_clickable(By.ID, "login_btn")
            print("Found login button:", submit_button)

            username_field.send_keys("testuser000")
            password_field.send_keys("testpassword")
            submit_button.click()


            success_message = self.wait_for_element(By.XPATH, "//a[contains(text(), 'Hello, testuser')]")
            self.assertIn("Hello, testuser", success_message.text)
        except Exception as e:
            print("Error in test_2_login")
            print("Exception message:", str(e))
            print(driver.page_source) 
            raise e

    def test_3_navigate_links(self):
        driver = self.driver

        try:


            self.wait_for_element(By.LINK_TEXT, "Home")

            navbar_links = {
                "Home": "/index",
                "Introductory": "/leaderboard.html",
                "Profile": "/userinfo"
            }
            for link_text, url in navbar_links.items():
                driver.find_element(By.LINK_TEXT, link_text).click()
                time.sleep(1)  
                print("Navigated to:", driver.current_url)
                self.assertEqual(driver.current_url, f"http://127.0.0.1:5000{url}")
        except Exception as e:
            print("Error in test_3_navigate_links")
            print("Exception message:", str(e))
            print(driver.page_source)  
            raise e


if __name__ == "__main__":
    unittest.main()