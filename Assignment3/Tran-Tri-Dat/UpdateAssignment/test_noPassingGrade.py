# Generated by Selenium IDE
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

class TestPassingGrade():
  def setup_method(self, method):
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument("--private-window")
    self.driver = webdriver.Firefox(options=firefox_options)
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_passingGrade(self):
    # Test name: test_passingGrade
    # Step # | name | target | value
    # 1 | open | https://school.moodledemo.net/ | 
    self.driver.get("https://school.moodledemo.net/")
    # 2 | click | css=.login > a | 
    self.driver.find_element(By.CSS_SELECTOR, ".login > a").click()
    # 3 | type | id=username | teacher
    self.driver.find_element(By.ID, "username").send_keys("teacher")
    # 4 | type | id=password | moodle
    self.driver.find_element(By.ID, "password").send_keys("moodle")
    # 5 | click | id=loginbtn | 
    self.driver.find_element(By.ID, "loginbtn").click()
    # 6 | waitForElementPresent | css=.card:nth-child(9) .card-img | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".card:nth-child(9) .card-img")))
    # 7 | runScript | window.scrollTo(0,0.5) | 30000
    self.driver.execute_script("window.scrollTo(0,0.5)")
    # 8 | click | css=.card:nth-child(9) .card-img | 
    self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(9) .card-img").click()
    # 9 | click | name=setmode | 
    self.driver.find_element(By.NAME, "setmode").click()
    # 10 | waitForElementPresent | css=#coursecontentcollapse0 .activity-add-text | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#coursecontentcollapse0 .activity-add-text")))
    # 11 | click | css=#coursecontentcollapse0 .activity-add-text | 
    self.driver.find_element(By.CSS_SELECTOR, "#coursecontentcollapse0 .activity-add-text").click()
    # 12 | waitForElementPresent | linkText=Assignment | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Assignment")))
    # 13 | click | linkText=Assignment | 
    self.driver.find_element(By.LINK_TEXT, "Assignment").click()
    # 14 | type | id=id_name | Assignment 1
    self.driver.find_element(By.ID, "id_name").send_keys("Assignment 1")
    # 15 | click | id=id_submitbutton2 | 
    self.driver.find_element(By.ID, "id_submitbutton2").click()

    # 16 | waitForElementPresent | linkText=Assignment 1 | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Assignment 1")))
    # 17 | click | linkText=Assignment 1 | 
    self.driver.find_element(By.LINK_TEXT, "Assignment 1").click()
    # 18 | waitForElementPresent | linkText=Settings | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.LINK_TEXT, "Settings")))
    # 19 | click | linkText=Settings | 
    self.driver.find_element(By.LINK_TEXT, "Settings").click()

    # 20 | waitForElementPresent 
    WebDriverWait(self.driver, 30).until(expected_conditions.presence_of_element_located((By.ID, "collapseElement-10")))

    # 21 | click | id=collapseElement-10 | 
    # Check if the user menu is already open
    is_user_menu_open = self.driver.find_element(By.ID, "collapseElement-10").get_attribute("aria-expanded") == "true"
    # Click the toggle only if it's not open
    if not is_user_menu_open:
        self.driver.find_element(By.ID, "collapseElement-10").click()
    # 22 | click | id=id_completion_2 | 
    self.driver.find_element(By.ID, "id_completion_2").click()
    # 23 | click | id=id_completionusegrade | 
    self.driver.find_element(By.ID, "id_completionusegrade").click()
    # 24 | click | id=id_completionpassgrade_1 | 
    self.driver.find_element(By.ID, "id_completionpassgrade_1").click()

    # 25 | click | id=id_submitbutton | 
    self.driver.find_element(By.ID, "id_submitbutton").click()

    # 26 | assertErrorDisplayed
    elements = self.driver.find_elements(By.ID, "id_error_completionpassgrade_1")
    assert len(elements) > 0, "Error not displayed"

    # 27 | waitForElementVisible | css=#carousel-item-main > .dropdown-item:nth-child(12) | 30000
    WebDriverWait(self.driver, 30).until(expected_conditions.visibility_of_element_located((By.CSS_SELECTOR, "#carousel-item-main > .dropdown-item:nth-child(12)")))
    # 28 | click | css=#carousel-item-main > .dropdown-item:nth-child(12) | 
    self.driver.find_element(By.CSS_SELECTOR, "#carousel-item-main > .dropdown-item:nth-child(12)").click()
  
if __name__ == "__main__":
  pytest.main()