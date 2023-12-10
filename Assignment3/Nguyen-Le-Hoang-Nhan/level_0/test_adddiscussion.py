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


class TestAdddiscussion:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(30)
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_adddiscussionnormal(self):
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1200, 1006)
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("teacher")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("test")
        self.driver.find_element(By.ID, "loginbtn").click()
        self.driver.find_element(By.LINK_TEXT, "My courses").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".multiline > span:nth-child(2)"
        ).click()
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        self.driver.find_element(By.LINK_TEXT, "Add discussion topic").click()
        self.driver.find_element(By.ID, "id_subject").click()
        self.driver.find_element(By.ID, "id_subject").send_keys("Test")
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "id_message_ifr"))
        self.driver.find_element(By.CSS_SELECTOR, "html").click()
        element = self.driver.find_element(By.ID, "tinymce")
        self.driver.execute_script(
            "if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Test'}",
            element,
        )
        self.driver.switch_to.default_content()
        self.driver.find_element(By.ID, "id_submitbutton").click()
        self.driver.find_element(By.XPATH, "//th/div/div/a").click()
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".flex-column > .font-weight-bold"
            ).text
            == "Test"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".post-content-container > p"
            ).text
            == "Test"
        )
        self.driver.find_element(By.LINK_TEXT, "Delete").click()
        self.driver.find_element(By.XPATH, "//button[contains(.,'Continue')]").click()
        self.driver.find_element(By.ID, "user-menu-toggle").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()

    def test_adddiscussionwithtoolongtopic(self):
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1200, 1006)
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("teacher")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("test")
        self.driver.find_element(By.ID, "loginbtn").click()
        self.driver.find_element(By.LINK_TEXT, "My courses").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".multiline > span:nth-child(2)"
        ).click()
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        self.driver.find_element(By.LINK_TEXT, "Add discussion topic").click()
        self.driver.find_element(By.ID, "id_subject").click()
        self.driver.find_element(By.ID, "id_subject").send_keys(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque in rutrum erat. Integer commodo est ut scelerisque semper. In consectetur, quam non eleifend cursus, risus orci fringilla augue, non finibus libero dui ac libero. Praesent sagittis magna sit amet porta feugiat. Suspendisse non tincidunt nunc. Maecenas pulvinar eleifend pellentesque. Mauris sit amet odio sed quam feugiat mattis. Fusce gravida cursus faucibus. Aliquam in nibh non nibh pellentesque feugiat non nec massa.  Vivamus imperdiet sagittis ex, at euismod diam maximus nec. Morbi dignissim tincidunt felis, non tincidunt tellus vehicula id. Nulla quis euismod metus, quis sollicitudin mi. Duis vel imperdiet turpis, eget molestie lectus. Quisque pretium vehicula lacinia. Cras enim dui, accumsan eget suscipit at, iaculis at orci. In purus massa, commodo et quam a, venenatis blandit augue. Sed volutpat erat vitae felis aliquam tincidunt. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Integer eu erat ligula.  Proin felis velit, accumsan eu eros et, blandit placerat felis. Donec cursus nisl at ex vestibulum imperdiet. Nullam ut lorem dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut a eleifend ante. Cras egestas, orci sit amet congue mollis, est nibh dignissim orci, sed suscipit purus neque quis arcu. Fusce eros purus, venenatis nec mollis vitae, rutrum et quam. Proin enim metus, dignissim sed augue a, hendrerit pretium urna. Pellentesque luctus, sem non pellentesque tempor, dolor turpis vehicula magna, et bibendum tortor ligula eu libero. Cras volutpat malesuada metus, sit amet tincidunt augue volutpat in. Sed ut rutrum arcu, at mattis orci. Cras viverra leo nec erat condimentum, et pharetra enim tincidunt. Nam."
        )
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "id_message_ifr"))
        self.driver.find_element(By.CSS_SELECTOR, "html").click()
        element = self.driver.find_element(By.ID, "tinymce")
        self.driver.execute_script(
            "if(arguments[0].contentEditable === 'true') {arguments[0].innerText = '<p>Test</p>'}",
            element,
        )
        self.driver.switch_to.default_content()
        assert (
            self.driver.find_element(By.ID, "id_error_subject").text
            == "- Maximum of 255 characters"
        )
        self.driver.find_element(By.ID, "id_submitbutton").click()
        self.driver.find_element(By.CSS_SELECTOR, ".userbutton").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()

    def test_attachafiletoadiscussion(self):
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1200, 1006)
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("teacher")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("test")
        self.driver.find_element(By.ID, "loginbtn").click()
        self.driver.find_element(By.LINK_TEXT, "My courses").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".multiline > span:nth-child(2)"
        ).click()
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        self.driver.find_element(By.LINK_TEXT, "Add discussion topic").click()
        self.driver.find_element(By.ID, "id_advancedadddiscussion").click()
        self.driver.find_element(By.ID, "id_subject").click()
        self.driver.find_element(By.ID, "id_subject").send_keys("Test")
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "id_message_ifr"))
        self.driver.find_element(By.CSS_SELECTOR, "html").click()
        self.driver.find_element(By.XPATH, "//body[@id='tinymce']").click()
        element = self.driver.find_element(By.ID, "tinymce")
        self.driver.execute_script(
            "if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Test'}",
            element,
        )
        self.driver.switch_to.default_content()
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()
        self.driver.find_element(By.LINK_TEXT, "Upload a file").click()
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys(
            "/Users/nhanlenguyen/Downloads/test.txt"
        )
        self.driver.find_element(
            By.XPATH, "//button[contains(.,'Upload this file')]"
        ).click()
        self.driver.find_element(By.ID, "id_submitbutton").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".discussion:nth-child(1) .w-100"
        ).click()
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".flex-column > .font-weight-bold"
            ).text
            == "Test"
        )
        assert (
            self.driver.find_element(
                By.CSS_SELECTOR, ".post-content-container > p"
            ).text
            == "Test"
        )
        assert (
            self.driver.find_element(By.CSS_SELECTOR, ".no-overflow > div > a").text
            == "test.txt"
        )
        self.driver.find_element(By.LINK_TEXT, "Delete").click()
        self.driver.find_element(By.XPATH, "//button[contains(.,'Continue')]").click()
        self.driver.find_element(By.ID, "user-menu-toggle").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()

    def test_attachafiletoadiscussionwithtoolongdiscussionname(self):
        self.driver.get("http://localhost:8000/")
        self.driver.set_window_size(1200, 1006)
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").click()
        self.driver.find_element(By.ID, "username").send_keys("teacher")
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("test")
        self.driver.find_element(By.ID, "loginbtn").click()
        self.driver.find_element(By.LINK_TEXT, "My courses").click()
        self.driver.find_element(
            By.CSS_SELECTOR, ".multiline > span:nth-child(2)"
        ).click()
        self.driver.find_element(By.LINK_TEXT, "Forum").click()
        self.driver.find_element(By.LINK_TEXT, "Add discussion topic").click()
        self.driver.find_element(By.ID, "id_advancedadddiscussion").click()
        self.driver.find_element(By.ID, "id_subject").click()
        self.driver.find_element(By.ID, "id_subject").send_keys(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque in rutrum erat. Integer commodo est ut scelerisque semper. In consectetur, quam non eleifend cursus, risus orci fringilla augue, non finibus libero dui ac libero. Praesent sagittis magna sit amet porta feugiat. Suspendisse non tincidunt nunc. Maecenas pulvinar eleifend pellentesque. Mauris sit amet odio sed quam feugiat mattis. Fusce gravida cursus faucibus. Aliquam in nibh non nibh pellentesque feugiat non nec massa.\\n\\nVivamus imperdiet sagittis ex, at euismod diam maximus nec. Morbi dignissim tincidunt felis, non tincidunt tellus vehicula id. Nulla quis euismod metus, quis sollicitudin mi. Duis vel imperdiet turpis, eget molestie lectus. Quisque pretium vehicula lacinia. Cras enim dui, accumsan eget suscipit at, iaculis at orci. In purus massa, commodo et quam a, venenatis blandit augue. Sed volutpat erat vitae felis aliquam tincidunt. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Integer eu erat ligula.\\n\\nProin felis velit, accumsan eu eros et, blandit placerat felis. Donec cursus nisl at ex vestibulum imperdiet. Nullam ut lorem dolor. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut a eleifend ante. Cras egestas, orci sit amet congue mollis, est nibh dignissim orci, sed suscipit purus neque quis arcu. Fusce eros purus, venenatis nec mollis vitae, rutrum et quam. Proin enim metus, dignissim sed augue a, hendrerit pretium urna. Pellentesque luctus, sem non pellentesque tempor, dolor turpis vehicula magna, et bibendum tortor ligula eu libero. Cras volutpat malesuada metus, sit amet tincidunt augue volutpat in. Sed ut rutrum arcu, at mattis orci. Cras viverra leo nec erat condimentum, et pharetra enim tincidunt. Nam."
        )
        self.driver.switch_to.frame(self.driver.find_element(By.ID, "id_message_ifr"))
        self.driver.find_element(By.CSS_SELECTOR, "html").click()
        self.driver.find_element(By.XPATH, "//body[@id='tinymce']").click()
        element = self.driver.find_element(By.ID, "tinymce")
        self.driver.execute_script(
            "if(arguments[0].contentEditable === 'true') {arguments[0].innerText = 'Test'}",
            element,
        )
        self.driver.switch_to.default_content()
        self.driver.find_element(By.CSS_SELECTOR, ".fa-file-o").click()
        self.driver.find_element(By.LINK_TEXT, "Upload a file").click()
        self.driver.find_element(By.NAME, "repo_upload_file").send_keys(
            "/Users/nhanlenguyen/Downloads/test.txt"
        )
        self.driver.find_element(
            By.XPATH, "//button[contains(.,'Upload this file')]"
        ).click()
        self.driver.find_element(By.ID, "id_submitbutton").click()
        assert (
            self.driver.find_element(By.ID, "id_error_subject").text
            == "- Maximum of 255 characters"
        )
        self.driver.find_element(By.ID, "user-menu-toggle").click()
        self.driver.find_element(By.LINK_TEXT, "Log out").click()