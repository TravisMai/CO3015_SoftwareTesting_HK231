import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestEquivalenceWithExceedFileSize:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()
        
    def test_exceed_file_size(self):
        self.driver.get("https://school.moodledemo.net/my/courses.php")
        self.driver.set_window_size(1198, 593)
        self.driver.find_element(By.CSS_SELECTOR, ".userpicture").click()
        self.driver.find_element(By.LINK_TEXT, "Private files").click()
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()
        self.driver.find_element(By.NAME, "repo_upload_file").click()

        # Upload a file that exceeds the maximum allowed size
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys("C:\\fakepath\\large_file.pdf")

        self.driver.find_element(By.ID, "yui_3_18_1_1_1702117389891_793").click()

        # Check for the expected error message
        error_message = self.driver.find_element(By.CSS_SELECTOR, ".error").text
        expected_error_message = "413 (Payload Too Large)"

        assert expected_error_message in error_message, f"Expected error message not found. Actual error message: {error_message}"