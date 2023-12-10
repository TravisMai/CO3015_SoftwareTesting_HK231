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

class TestDataDrivenNotifications:

    @pytest.fixture
    def setup_teardown(self):
        self.driver = webdriver.Chrome()
        self.vars = {}
        yield
        self.driver.quit()

    @pytest.mark.parametrize("notification_index, preference_index", [(2, 2), (2, 3), (2, 2), (2, 3)])
    def test_notification_assignment(self, setup_teardown, notification_index, preference_index):
        # Test name: Notification_Assignment
        # Step # | name | target | value
        # 1 | open | https://school.moodledemo.net/my/courses.php |
        self.driver.get("https://school.moodledemo.net/my/courses.php")
        # 2 | setWindowSize | 1688x1045 |
        self.driver.set_window_size(1688, 1045)
        # 3 | click | css=.fa-bell-o |
        self.driver.find_element(By.CSS_SELECTOR, ".fa-bell-o").click()
        # 4 | click | css=a:nth-child({notification_index}) > .fa-cog |
        self.driver.find_element(By.CSS_SELECTOR, f"a:nth-child({notification_index}) > .fa-cog").click()
        # 5 | click | css=.preference-row:nth-child(2) > td:nth-child({preference_index}) .custom-control-label |
        self.driver.find_element(By.CSS_SELECTOR, f".preference-row:nth-child(2) > td:nth-child({preference_index}) .custom-control-label").click()
        # 6 | click | linkText=Dashboard |
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        # 7 | close | |
        self.driver.close()
