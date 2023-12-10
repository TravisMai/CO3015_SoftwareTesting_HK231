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

class TestEquivalenceWithNormalFileSize:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_equivalence_with_normal_file_size(self):
        self.driver.get("https://school.moodledemo.net/my/courses.php")
        self.driver.set_window_size(1198, 593)
        self.driver.find_element(By.CSS_SELECTOR, ".userpicture").click()
        self.driver.find_element(By.LINK_TEXT, "Private files").click()
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()
        self.driver.find_element(By.NAME, "repo_upload_file").click()

        # Upload an empty file (0 bytes)
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys("C:\\fakepath\\normal_file.txt")

        self.driver.find_element(By.ID, "yui_3_18_1_1_1702117389891_793").click()
        self.driver.find_element(By.NAME, "submitbutton").click()

        # Check for successful upload message
        success_message = self.driver.find_element(By.CSS_SELECTOR, ".success").text
        expected_success_message = "File uploaded successfully."

        assert expected_success_message in success_message, f"Expected success message not found. Actual success message: {success_message}"
