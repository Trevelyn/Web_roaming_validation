import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time

class Cross_process(unittest.TestCase):

    def setUp(self):
        """Set up Chrome and Edge drivers."""
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            self.chrome_driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=chrome_options)
            self.chrome_driver.set_window_size(945, 1012)
        except Exception as e:
            print(f"Error during Chrome setup: {e}")
            self.chrome_driver = None

        try:
            edge_options = webdriver.EdgeOptions()
            edge_options.add_argument("-inprivate")
            self.edge_driver = webdriver.Edge(service=webdriver.edge.service.Service(EdgeChromiumDriverManager().install()), options=edge_options)
            self.edge_driver.set_window_size(945, 1012)
        except Exception as e:
            print(f"Error during Edge setup: {e}")
            self.edge_driver = None

    def tearDown(self):
        """Tear down the drivers after tests."""
        if self.chrome_driver:
            self.chrome_driver.quit()
        if self.edge_driver:
            self.edge_driver.quit()

    def login_and_authenticate(self, driver):
        """Login and authenticate the user in the specified driver."""
        if driver is None:
            return
        try:
            driver.get("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=95de633a-083e-42f5-b444-a4295d8e9314&scope=openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fwhiteboard.office.com%2Fmsalv2redirect%2F&client-request-id=a8aaaed1-8c3d-474c-8362-d2eab705db2b&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.33.0&client_info=1&code_challenge=7HUBeVEYTl_-ByIXjVQhO2knL0KkaST8F6q4IHwz3yE&code_challenge_method=S256&prompt=select_account&nonce=10a4ce50-b54c-4dbd-8af8-38d85db768f1&state=eyJpZCI6IjQ5NGRkZWUwLTBiYjgtNDAxMi05OTUwLTY5ZTZjOWYwYjI3MCIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D&claims=%7B%22access_token%22%3A%7B%22xms_cc%22%3A%7B%22values%22%3A%5B%22cp1%22%5D%7D%7D%7D&sso_reload=true")
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "i0116"))).send_keys("IsaiahL@M365x41049209.OnMicrosoft.com" + Keys.ENTER)
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "i0118"))).send_keys("Kenya@2023" + Keys.ENTER)
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "signInAnotherWay"))).click()
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".row:nth-child(3) .text-left > div"))).click()
            time.sleep(2)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idTxtBx_SAOTCC_OTC"))).click()
            print("Waiting for user to enter authentication code...")
            time.sleep(30)
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "idSubmit_SAOTCC_Continue"))).click()
        except TimeoutException:
            print(f"Element not found or timed out.")
        except Exception as e:
            print(f"Error during login and authentication: {e}")

    def toggle_connected_experience(self, driver, expected_state):
        """Toggle the connected experience setting and verify its state."""
        if driver is None:
            return
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, "boardPickerSettingsButton"))).click()
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//li[5]/button/div/span"))).click()
            toggle_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@role='switch' and contains(@aria-label, 'Toggle optional connected experiences')]")))
            current_state = toggle_button.get_attribute("aria-checked")
            expected_state = "true" if expected_state == "true" else "false"
            if current_state != expected_state:
                toggle_button.click()
                WebDriverWait(driver, 30).until(lambda d: toggle_button.get_attribute("aria-checked") == expected_state)
                self.assertEqual(toggle_button.get_attribute("aria-checked"), expected_state, f"Toggle did not switch to the expected state: aria-checked='{expected_state}'")
            else:
                print(f"Toggle is already in the expected state: aria-checked='{expected_state}'")
        except TimeoutException:
            print("Element timed out while trying to toggle connected experience.")
        except Exception as e:
            print(f"Error during toggling connected experience: {e}")

    def test_roaming_settings(self):
        """Test to verify the roaming settings between Chrome and Edge."""
        self.login_and_authenticate(self.chrome_driver)
        self.toggle_connected_experience(self.chrome_driver, "true")
        time.sleep(30)
        self.login_and_authenticate(self.edge_driver)
        chrome_toggle_state = WebDriverWait(self.chrome_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@role='switch' and contains(@class, 'ms-Toggle-background')]"))
        ).get_attribute("aria-checked")
        self.assertEqual(chrome_toggle_state, "true", "Initial Chrome toggle state is not 'true'")
        self.toggle_connected_experience(self.edge_driver, "true")
        self.toggle_connected_experience(self.chrome_driver, "false")
        time.sleep(30)
        self.edge_driver.refresh()
        time.sleep(10)
        edge_toggle_state = WebDriverWait(self.edge_driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[@role='switch' and contains(@class, 'ms-Toggle-background')]"))
        ).get_attribute("aria-checked")
        self.assertEqual(edge_toggle_state, "false", "Edge toggle state did not sync to match Chrome's toggle state.")

if __name__ == "__main__":
    unittest.main()
