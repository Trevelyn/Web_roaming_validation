import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time

class Cross_process(unittest.TestCase):

    def setUp(self):
        """Set up Chrome and Edge drivers."""
        try:
            # Initialize Chrome driver
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--incognito")
            self.chrome_driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=chrome_options)
            self.chrome_driver.set_window_size(945, 1012)
        except Exception as e:
            print(f"Error during Chrome setup: {e}")
            self.chrome_driver = None

        try:
            # Initialize Edge driver
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
            # Navigate to the login page
            driver.get("https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=95de633a-083e-42f5-b444-a4295d8e9314&scope=openid%20profile%20offline_access&redirect_uri=https%3A%2F%2Fwhiteboard.office.com%2Fmsalv2redirect%2F&client-request-id=a8aaaed1-8c3d-474c-8362-d2eab705db2b&response_mode=fragment&response_type=code&x-client-SKU=msal.js.browser&x-client-VER=2.33.0&client_info=1&code_challenge=7HUBeVEYTl_-ByIXjVQhO2knL0KkaST8F6q4IHwz3yE&code_challenge_method=S256&prompt=select_account&nonce=10a4ce50-b54c-4dbd-8af8-38d85db768f1&state=eyJpZCI6IjQ5NGRkZWUwLTBiYjgtNDAxMi05OTUwLTY5ZTZjOWYwYjI3MCIsIm1ldGEiOnsiaW50ZXJhY3Rpb25UeXBlIjoicmVkaXJlY3QifX0%3D&claims=%7B%22access_token%22%3A%7B%22xms_cc%22%3A%7B%22values%22%3A%5B%22cp1%22%5D%7D%7D%7D&sso_reload=true")

            # Retry logic for finding and interacting with elements to avoid stale references
            def safe_find_element(driver, by, value, retries=3):
                for _ in range(retries):
                    try:
                        element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))
                        return element
                    except StaleElementReferenceException:
                        print("Stale element, retrying...")
                raise Exception(f"Element {value} not stable after {retries} retries")
            
            # Enter email and proceed
            email_input = safe_find_element(driver, By.ID, "i0116")
            email_input.send_keys("IsaiahL@M365x41049209.OnMicrosoft.com")
            email_input.send_keys(Keys.ENTER)

            # Enter password and proceed
            password_input = safe_find_element(driver, By.ID, "i0118")
            password_input.send_keys("Kenya@2023")
            password_input.send_keys(Keys.ENTER)

            sign_in_button = safe_find_element(driver, By.XPATH, "//input[@id='idSIButton9']")
            sign_in_button.click()

            # Select "Sign in another way"
            sign_in_another_way_button = safe_find_element(driver, By.ID, "signInAnotherWay")
            sign_in_another_way_button.click()

            # Select the third option
            third_option = safe_find_element(driver, By.CSS_SELECTOR, ".row:nth-child(3) .text-left > div")
            third_option.click()

            # Click on the authentication code field
            auth_code_field = safe_find_element(driver, By.ID, "idTxtBx_SAOTCC_OTC")
            auth_code_field.click()

            # Wait for the user to manually enter the authentication code
            time.sleep(30)  # Adjust sleep time based on how long it takes to receive the 2FA code

            # Click continue after entering the authentication code
            continue_button = safe_find_element(driver, By.ID, "idSubmit_SAOTCC_Continue")
            continue_button.click()
            
        except TimeoutException:
            print(f"Element not found or timed out.")
        except Exception as e:
            print(f"Error during login and authentication: {e}")


    def toggle_connected_experience(self, driver, expected_state):
        """Toggle the connected experience setting and verify its state."""
        if driver is None:
            return
        try:
            # Wait and click the settings button
            settings_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "boardPickerSettingsButton")))
            settings_button.click()

            # Wait for and click the privacy button
            privacy_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//li[5]/button/div/span")))
            privacy_button.click()

            # Locate the toggle button and check its current state
            toggle_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div/div[3]/div[2]/div[2]/div/button")))
            current_state = toggle_button.get_attribute("aria-checked")

            # Convert expected_state to string for consistent comparison
            expected_state = "true" if expected_state == "true" else "false"

            # If the current state is not as expected, click to change it
            if current_state != expected_state:
                toggle_button.click()
                # Wait for the toggle state to change
                WebDriverWait(driver, 10).until(
                    lambda d: toggle_button.get_attribute("aria-checked") == expected_state
                )
                # Verify the state is now the expected one
                self.assertEqual(toggle_button.get_attribute("aria-checked"), expected_state,
                                f"Toggle did not switch to the expected state: aria-checked='{expected_state}'")
            else:
                print(f"Toggle is already in the expected state: aria-checked='{expected_state}'")

        except TimeoutException:
            print("Element timed out while trying to toggle connected experience.")
        except Exception as e:
            print(f"Error during toggling connected experience: {e}")

    def test_roaming_settings(self):
        """Test to verify the roaming settings between Chrome and Edge."""
        # Login and authenticate in Chrome
        self.login_and_authenticate(self.chrome_driver)
        
        # Turn off the connected experience in Chrome
        self.toggle_connected_experience(self.chrome_driver, "false")

        # Sleep to allow settings to take effect
        time.sleep(30)

        # Login and authenticate in Edge
        self.login_and_authenticate(self.edge_driver)

        # Verify the toggle state in Edge
        self.toggle_connected_experience(self.edge_driver, "false")
        time.sleep(30)

        # Switch back to Chrome and activate the toggle
        self.toggle_connected_experience(self.chrome_driver, "true")

        # Sleep to allow settings to take effect
        time.sleep(30)
        # Refresh Edge and verify the toggle state again
        if self.edge_driver is not None:
            self.edge_driver.refresh()
            WebDriverWait(self.edge_driver, 30).until(EC.presence_of_element_located((By.ID, "boardPickerSettingsButton")))
            settings_button = self.edge_driver.find_element(By.ID, "boardPickerSettingsButton")
            settings_button.click()

            # Move to the privacy button and click it
            actions = ActionChains(self.edge_driver)
            actions.move_to_element(settings_button).perform()

            privacy_button = self.edge_driver.find_element(By.XPATH, ".//li[5]/button/div/span")
            privacy_button.click()

            # Verify the toggle state in Edge using the XPath
            toggle_state_edge_after = self.edge_driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div/div[3]/div[2]/div[2]/div/button").get_attribute("aria-checked")
            self.assertEqual(toggle_state_edge_after, "true", "Edge toggle is not the same as Chrome toggle")

            # Switch back to Chrome and turn off the toggle
            self.toggle_connected_experience(self.chrome_driver, "false")

            # Sleep to allow settings to take effect
            time.sleep(30)

            # Refresh Edge and verify the toggle state again
            self.edge_driver.refresh()
            WebDriverWait(self.edge_driver, 5).until(EC.presence_of_element_located((By.ID, "boardPickerSettingsButton")))
            settings_button = self.edge_driver.find_element(By.ID, "boardPickerSettingsButton")
            settings_button.click()

            # Move to the privacy button and click it
            actions = ActionChains(self.edge_driver)
            actions.move_to_element(settings_button).perform()

            privacy_button = self.edge_driver.find_element(By.XPATH, "//li[5]/button/div/span")
            privacy_button.click()

            # Verify the toggle state in Edge using the XPath
            toggle_state_edge_final = self.edge_driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div/div[3]/div[2]/div[2]/div/button").get_attribute("aria-checked")
            self.assertEqual(toggle_state_edge_final, "false", "Edge toggle is not the same as Chrome toggle")


if __name__ == "__main__":
    unittest.main()
