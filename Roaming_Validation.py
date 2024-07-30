import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeRoamingValidation(unittest.TestCase):

    def setUp(self):
        try:
            # Use ChromeDriverManager to manage ChromeDriver installation
            self.driver = webdriver.Chrome()
            self.driver.set_window_size(945, 1012)
        except Exception as e:
            print(f"Error during setup: {e}")
            self.tearDown()

    def tearDown(self):
        if self.driver:
            # Quit the browser after each test
            self.driver.quit()

    def test_get_chrome_page(self):
        try:
            self.driver.get("https://whiteboard.office.com/?source=applauncher&auth_upn=IsaiahL%40M365x54705503.OnMicrosoft.com")
            
            # Wait until the frame is available and switch to it
            WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe"))
            )
        except Exception as e:
            print(f"Error during opening whiteboard: {e}")
            self.tearDown()
        
        try:
            # Wait for and click the settings button
            wait = WebDriverWait(self.driver, 10)
            settings_button = wait.until(EC.element_to_be_clickable((By.ID, "boardPickerSettingsButton")))
            settings_button.click()
            
            # Perform actions with ActionChains
            actions = ActionChains(self.driver)
            actions.move_to_element(settings_button).perform()

            # Select Privacy settings
            body_element = self.driver.find_element(By.CSS_SELECTOR, "body")
            actions.move_to_element(body_element, 0, 0).perform()
            privacy_button = self.driver.find_element(By.CSS_SELECTOR, ".privacyAndSecurityButton .ms-ContextualMenu-itemText")
            privacy_button.click()

            # Switch the toggle off
            toggle_element = self.driver.find_element(By.CSS_SELECTOR, "#Toggle65 > .ms-Toggle-thumb")
            toggle_element.click()

            # Assertion to verify optional connected experience is switched off
            toggle_state = self.driver.find_element(By.CSS_SELECTOR, "#Toggle65").get_attribute("aria-checked")
            self.assertEqual(toggle_state, "false", "Toggle65 is not switched off")

            close_button = self.driver.find_element(By.ID, "undefinedCloseButton")
            close_button.click()
                 
        except Exception as e:
            print(f"Error during test: {e}")
            self.tearDown()

if __name__ == "__main__":
    unittest.main()
