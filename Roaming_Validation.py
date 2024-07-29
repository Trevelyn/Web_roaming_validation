import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChromeRoamingValidation(unittest.TestCase):

    def setUp(self):
        # Use ChromeDriverManager to manage ChromeDriver installation
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.set_window_size(945, 1012)

    def tearDown(self):
        # Quit the browser after each test
        self.driver.quit()

    def test_get_chrome_page(self):
        self.driver.get("https://whiteboard.office.com/?source=applauncher&auth_upn=IsaiahL%40M365x54705503.OnMicrosoft.com")
        
        # Wait until the frame is available and switch to it
        WebDriverWait(self.driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe"))
        )

        # Assert and interact with elements on the page
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, "boardPickerSettingsButton"))).click()
        
        element = self.driver.find_element(By.ID, "boardPickerSettingsButton")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

        # Select Privacy settings
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions.move_to_element(element, 0, 0).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".privacyAndSecurityButton .ms-ContextualMenu-itemText").click()

        # Switch the toggle
        self.driver.find_element(By.CSS_SELECTOR, "#Toggle65 > .ms-Toggle-thumb").click()
        self.driver.find_element(By.ID, "undefinedCloseButton").click()
        
        # Repeating the steps to perform the necessary actions
        element = self.driver.find_element(By.ID, "boardPickerSettingsButton")
        actions.move_to_element(element).perform()
        self.driver.find_element(By.ID, "boardPickerSettingsButton").click()
        
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions.move_to_element(element, 0, 0).perform()
    
        element = self.driver.find_element(By.ID, "Toggle39")
        actions.move_to_element(element).perform()
        
        element = self.driver.find_element(By.CSS_SELECTOR, "body")
        actions.move_to_element(element, 0, 0).perform()
       
        self.driver.find_element(By.CSS_SELECTOR, ".privacyAndSecurityButton .ms-ContextualMenu-itemText").click()
        self.driver.find_element(By.ID, "undefinedCloseButton").click()

if __name__ == "__main__":
    unittest.main()



