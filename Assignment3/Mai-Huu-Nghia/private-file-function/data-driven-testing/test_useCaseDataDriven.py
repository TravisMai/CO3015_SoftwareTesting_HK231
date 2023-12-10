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

class TestUsecaseUploadFileScenarios:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    @pytest.mark.parametrize("use_case_path, file_path", [
        ("P1", "C:\\fakepath\\50MB_file_upload1.pdf"),
        ("P2", "C:\\fakepath\\50MB_file_upload2.pdf")
    ])
    def test_upload_file_scenarios(self, use_case_path, file_path):
        # Pre-condition: Login as the user (You can add login steps here)

        self.driver.get("https://school.moodledemo.net/my/courses.php")
        self.driver.set_window_size(1198, 593)
        self.driver.find_element(By.CSS_SELECTOR, ".userpicture").click()
        self.driver.find_element(By.LINK_TEXT, "Private files").click()
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()

        # Normal flow based on the use case path
        if use_case_path == "P1":
            # Use Case P1: Click on the Add icon and choose file to upload
            self.driver.find_element(By.NAME, "repo_upload_file").click()
            self.driver.find_element(By.NAME, "repo_upload_file").send_keys(file_path)
            self.driver.find_element(By.ID, "yui_3_18_1_1_1702117389891_793").click()
        elif use_case_path == "P2":
            # Use Case P2: Drag the file to the upload section
            file_input = self.driver.find_element(By.NAME, "repo_upload_file")
            upload_section = self.driver.find_element(By.CSS_SELECTOR, ".filemanager-region.filemanager-region-upload")
            ActionChains(self.driver).drag_and_drop(file_input, upload_section).perform()

        # Common steps for both use cases
        self.driver.find_element(By.NAME, "submitbutton").click()

        # Check for the expected success message
        success_message = self.driver.find_element(By.CSS_SELECTOR, ".success").text
        expected_success_message = "File uploaded successfully."

        assert expected_success_message in success_message, f"Expected success message not found. Actual success message: {success_message}"
