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

class TestNotificationAssignment2():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_notificationAssignment2(self):
    # Test name: Notification_Assignment_2
    # Step # | name | target | value
    # 1 | open | https://school.moodledemo.net/my/courses.php | 
    self.driver.get("https://school.moodledemo.net/my/courses.php")
    # 2 | setWindowSize | 1688x1045 | 
    self.driver.set_window_size(1688, 1045)
    # 3 | click | css=.fa-bell-o | 
    self.driver.find_element(By.CSS_SELECTOR, ".fa-bell-o").click()
    # 4 | click | css=a:nth-child(2) > .fa-cog | 
    self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .fa-cog").click()
    # 5 | click | css=.preference-row:nth-child(2) > td:nth-child(3) .custom-control-label | 
    self.driver.find_element(By.CSS_SELECTOR, ".preference-row:nth-child(2) > td:nth-child(3) .custom-control-label").click()
    # 6 | click | linkText=Dashboard | 
    self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
    # 7 | close |  | 
    self.driver.close()
  
