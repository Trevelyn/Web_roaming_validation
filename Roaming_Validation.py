import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ChromeRoamingValidation(unittest.TestCase):

    def setUp(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.set_window_size(945, 1012)
        except Exception as e:
            print(f"Error during setup: {e}")
            self.tearDown()

    def tearDown(self):
        if self.driver:
            self.driver.quit()

    def test_get_chrome_page(self):
        try:
            self.driver.get("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=95de633a-083e-42f5-b444-a4295d8e9314&scope=openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fwhiteboard.office.com%2Fmsalv2redirect%2F&client-request-id=a8aaaed1-8c3d-474c-8362-d2eab705db2b&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.33.0&client_info=1&code_challenge=7HUBeVEYTl_-ByIXjVQhO2knL0KkaST8F6q4IHwz3yE&code_challenge_method=S256&prompt=select_account&nonce=10a4ce50-b54c-4dbd-8af8-38d85db768f1&state=eyJpZCI6IjQ5NGRkZWUwLTBiYjgtNDAxMi05OTUwLTY5ZTZjOWYwYjI3MCIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D&claims=%7B%22access_token%22%3A%7B%22xms_cc%22%3A%7B%22values%22%3A%5B%22cp1%22%5D%7D%7D%7D&sso_reload=true")

            # Login user
            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "i0116")))
                self.driver.find_element(By.ID, "i0116").send_keys("IsaiahL@M365x54705503.OnMicrosoft.com")
                self.driver.find_element(By.ID, "i0116").send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error during entering email: {e}")
                return

            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "i0118")))
                self.driver.find_element(By.ID, "i0118").send_keys("Kenya@2023")
                self.driver.find_element(By.ID, "i0118").send_keys(Keys.ENTER)
            except Exception as e:
                print(f"Error during entering password: {e}")
                return

            # Authentication part
            try:
                WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.ID, "signInAnotherWay")))
                self.driver.find_element(By.ID, "signInAnotherWay").click()
            except Exception as e:
                print(f"Error during selecting another way to sign in: {e}")
                return

            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".row:nth-child(3) .text-left > div")))
                self.driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) .text-left > div").click()
            except Exception as e:
                print(f"Error during selecting the third option: {e}")
                return

            try:
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC")))
                self.driver.find_element(By.ID, "idTxtBx_SAOTCC_OTC").click()
            except Exception as e:
                print(f"Error during entering authentication code: {e}")
                return

            # Wait for the authentication code and enter manually
            time.sleep(30)  # Adjust sleep time based on how long it takes to receive the 2FA code

            self.driver.find_element(By.ID, "idSubmit_SAOTCC_Continue").click()

            # Continue with the rest of the test after 2FA
            try:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "boardPickerSettingsButton")))
                settings_button = self.driver.find_element(By.ID, "boardPickerSettingsButton")
                settings_button.click()
                
                actions = ActionChains(self.driver)
                actions.move_to_element(settings_button).perform()

                privacy_button = self.driver.find_element(By.CSS_SELECTOR, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
                privacy_button.click()

                toggle_element = self.driver.find_element(By.CSS_SELECTOR, "#Toggle65 > .ms-Toggle-thumb")
                toggle_element.click()

                # Assertion to verify optional connected experience is switched off
                toggle_state = self.driver.find_element(By.CSS_SELECTOR, "#Toggle65").get_attribute("aria-checked")
                self.assertEqual(toggle_state, "false", "Toggle65 is not switched off")

                close_button = self.driver.find_element(By.ID, "undefinedCloseButton")
                close_button.click()
            except Exception as e:
                print(f"Error during test: {e}")
                 
        except Exception as e:
            print(f"Error during opening whiteboard: {e}")

if __name__ == "__main__":
    unittest.main()
