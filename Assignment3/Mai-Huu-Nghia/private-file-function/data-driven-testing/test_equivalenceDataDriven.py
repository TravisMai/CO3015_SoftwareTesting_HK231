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

class TestEquivalenceFileUploadScenarios:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def navigate_to_upload_page(self):
        self.driver.get("https://school.moodledemo.net/my/courses.php")
        self.driver.set_window_size(1198, 593)
        self.driver.find_element(By.CSS_SELECTOR, ".userpicture").click()
        self.driver.find_element(By.LINK_TEXT, "Private files").click()
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()

    def perform_file_upload(self, file_path):
        self.driver.find_element(By.NAME, "repo_upload_file").click()
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys(file_path)
        self.driver.find_element(By.ID, "yui_3_18_1_1_1702117389891_793").click()

    def check_result_message(self, expected_message, message_type):
        actual_message = self.driver.find_element(By.CSS_SELECTOR, f".{message_type}").text
        assert expected_message in actual_message, f"Expected {message_type} message not found. Actual {message_type} message: {actual_message}"

    @pytest.mark.parametrize("file_path, expected_message", [
        ("C:\\fakepath\\empty_file.txt", "The uploaded file is empty."),
        ("C:\\fakepath\\normal_file.txt", "File uploaded successfully."),
        ("C:\\fakepath\\large_file.pdf", "413 (Payload Too Large)")
    ])
    def test_file_upload_scenarios(self, file_path, expected_message):
        self.navigate_to_upload_page()
        self.perform_file_upload(file_path)

        if "success" in expected_message.lower():
            self.check_result_message(expected_message, "success")
        elif "error" in expected_message.lower():
            self.check_result_message(expected_message, "error")
