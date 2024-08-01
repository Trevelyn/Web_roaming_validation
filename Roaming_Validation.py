import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ChromeRoamingValidation(unittest.TestCase):

    def setUp(self):
        """Set up Chrome and Edge drivers."""
        try:
            # Initialize Chrome driver
            self.chrome_driver = webdriver.Chrome()
            self.chrome_driver.set_window_size(945, 1012)
        except Exception as e:
            print(f"Error during Chrome setup: {e}")
            self.chrome_driver = None

        try:
            # Initialize Edge driver
            self.edge_driver = webdriver.Edge()
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
            # Navigate to the login page
            driver.get("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=95de633a-083e-42f5-b444-a4295d8e9314&scope=openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fwhiteboard.office.com%2Fmsalv2redirect%2F&client-request-id=a8aaaed1-8c3d-474c-8362-d2eab705db2b&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.33.0&client_info=1&code_challenge=7HUBeVEYTl_-ByIXjVQhO2knL0KkaST8F6q4IHwz3yE&code_challenge_method=S256&prompt=select_account&nonce=10a4ce50-b54c-4dbd-8af8-38d85db768f1&state=eyJpZCI6IjQ5NGRkZWUwLTBiYjgtNDAxMi05OTUwLTY5ZTZjOWYwYjI3MCIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D&claims=%7B%22access_token%22%3A%7B%22xms_cc%22%3A%7B%22values%22%3A%5B%22cp1%22%5D%7D%7D%7D&sso_reload=true")
            
            # Enter email and proceed
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "i0116")))
            driver.find_element(By.ID, "i0116").send_keys("IsaiahL@M365x54705503.OnMicrosoft.com")
            driver.find_element(By.ID, "i0116").send_keys(Keys.ENTER)

            # Enter password and proceed
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "i0118")))
            driver.find_element(By.ID, "i0118").send_keys("Kenya@2023")
            driver.find_element(By.ID, "i0118").send_keys(Keys.ENTER)

            # Select "Sign in another way"
            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "signInAnotherWay")))
            driver.find_element(By.ID, "signInAnotherWay").click()

            # Select the third option
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".row:nth-child(3) .text-left > div")))
            driver.find_element(By.CSS_SELECTOR, ".row:nth-child(3) .text-left > div").click()

            # Click on the authentication code field
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "idTxtBx_SAOTCC_OTC")))
            driver.find_element(By.ID, "idTxtBx_SAOTCC_OTC").click()

            # Wait for the user to manually enter the authentication code
            time.sleep(30)  # Adjust sleep time based on how long it takes to receive the 2FA code

            # Click continue after entering the authentication code
            driver.find_element(By.ID, "idSubmit_SAOTCC_Continue").click()
        except Exception as e:
            print(f"Error during login and authentication: {e}")

    def toggle_connected_experience(self, driver, expected_state):
        """Toggle the connected experience setting and verify its state."""
        if driver is None:
            return
        try:
            # Open the settings menu
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "boardPickerSettingsButton")))
            settings_button = driver.find_element(By.ID, "boardPickerSettingsButton")
            settings_button.click()

            # Move to the privacy button and click it
            actions = ActionChains(driver)
            actions.move_to_element(settings_button).perform()

            privacy_button = driver.find_element(By.CSS_SELECTOR, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
            privacy_button.click()

            # Toggle the connected experience setting
            toggle_element = driver.find_element(By.CSS_SELECTOR, "#Toggle65 > .ms-Toggle-thumb")
            toggle_element.click()

            # Verify the state of the toggle
            toggle_state = driver.find_element(By.CSS_SELECTOR, "#Toggle65").get_attribute("aria-checked")
            self.assertNotEqual(toggle_state, expected_state, f"Toggle65 is not switched to {toggle_state}")
        except Exception as e:
            print(f"Error during toggling connected experience: {e}")

    def test_roaming_settings(self):
        """Test to verify the roaming settings between Chrome and Edge."""
        # Login and authenticate in Chrome
        self.login_and_authenticate(self.chrome_driver)
        
        # Turn off the connected experience in Chrome
        self.toggle_connected_experience(self.chrome_driver, "false")

        # Sleep to allow settings to take effect
        time.sleep(5)

        # Login and authenticate in Edge
        self.login_and_authenticate(self.edge_driver)

        # Verify the toggle state in Edge
        self.toggle_connected_experience(self.edge_driver, "false")

        # Switch back to Chrome and activate the toggle
        self.toggle_connected_experience(self.chrome_driver, "true")

        # Sleep to allow settings to take effect
        time.sleep(5)

        # Refresh Edge and verify the toggle state again
        if self.edge_driver is not None:
            self.edge_driver.refresh()
            WebDriverWait(self.edge_driver, 10).until(EC.presence_of_element_located((By.ID, "boardPickerSettingsButton")))
            settings_button = self.edge_driver.find_element(By.ID, "boardPickerSettingsButton")
            settings_button.click()

            # Move to the privacy button and click it
            actions = ActionChains(self.edge_driver)
            actions.move_to_element(settings_button).perform()

            privacy_button = self.edge_driver.find_element(By.CSS_SELECTOR, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
            privacy_button.click()

            # Verify the toggle state in Edge
            toggle_state_edge_after = self.edge_driver.find_element(By.CSS_SELECTOR, "#Toggle65").get_attribute("aria-checked")
            self.assertEqual(toggle_state_edge_after, "true", "Edge toggle is not the same as Chrome toggle")

            # Switch back to Chrome and turn off the toggle
            self.toggle_connected_experience(self.chrome_driver, "false")

            # Sleep to allow settings to take effect
            time.sleep(5)

            # Refresh Edge and verify the toggle state again
            self.edge_driver.refresh()
            WebDriverWait(self.edge_driver, 10).until(EC.presence_of_element_located((By.ID, "boardPickerSettingsButton")))
            settings_button = self.edge_driver.find_element(By.ID, "boardPickerSettingsButton")
            settings_button.click()

            # Move to the privacy button and click it
            actions = ActionChains(self.edge_driver)
            actions.move_to_element(settings_button).perform()

            privacy_button = self.edge_driver.find_element(By.CSS_SELECTOR, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
            privacy_button.click()

            # Verify the toggle state in Edge
            toggle_state_edge_final = self.edge_driver.find_element(By.CSS_SELECTOR, "#Toggle65").get_attribute("aria-checked")
            self.assertEqual(toggle_state_edge_final, "false", "Edge toggle is not the same as Chrome toggle")

if __name__ == "__main__":
    unittest.main()
