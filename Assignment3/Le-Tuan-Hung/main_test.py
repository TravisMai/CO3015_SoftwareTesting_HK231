import unittest
import yaml
import os
import glob
import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from datetime import datetime
from time import sleep



class GoogleTestCase(unittest.TestCase):

    test_config = []
    test_report = {}
    time_stamp = datetime.now().strftime("%Y_%m_%d_%H%M%S")

    browser = {
        "chrome": webdriver.Chrome,
        "firefox": webdriver.Firefox,
        "edge": webdriver.Edge,
    }

    browser_options = {
        "chrome": webdriver.ChromeOptions,
        "firefox": webdriver.FirefoxOptions,
        "edge": webdriver.EdgeOptions,
    }

    def load_test_case(self):
        print("load test cases")
        files = glob.glob(os.path.dirname(os.path.abspath(__file__)) + "/testcases/*.yml")
        for filename in files:
            with open(filename) as file:
                self.test_config.append(yaml.safe_load(file))

    def setUp(self):
        self.options = webdriver.EdgeOptions()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--enable-chrome-browser-cloud-management")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--log-level=1")
        self.options.add_argument("--silent")
        self.options.add_argument("--show-capture=no")
        self.browser = webdriver.Edge(options=self.options)
        self.elem_dict = {"button":"button", "link":"a", "title":"title", "input":"input"}
        self.load_test_case()
        self.addCleanup(self.browser.quit)

    def execute_common_logic(self, step_config, action, actionchains, timeout=10):
        _type, key, value = step_config[0], step_config[1], step_config[2]
        by_type = getattr(By, _type.upper(), _type)
        try:
            if action == "click":
                if by_type == "CONTAIN":
                    xpath = (f"//{self.elem_dict[value]}[.//span[contains(text(), '{key}')]\
                            or @title='{key}' or @class='{key}' or descendant::div[contains(text(), '{key}')]\
                            or ancestor::div[contains(text(), '{key}')]]")
                    search_key = (By.XPATH, xpath)
                elif by_type == "TEXT":
                    xpath = f"//{self.elem_dict[value]}[contains(text(), '{key}') or contains(@placeholder, '{key}')]"
                    search_key = (By.XPATH, xpath)
                else:
                    search_key = (by_type, key)

                element = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_all_elements_located(search_key)
                )
                if len(element) > 0:
                    start_time = time.time()
                    while not element[0].is_displayed() and time.time() - start_time < timeout:
                        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    element[0].click()
                else:
                    result = False
                    msg = "Failed to appear or click on element within the specified timeout"
            elif action == "input":
                if by_type == "CONTAIN":
                    xpath = (f"//input[.//span[contains(text(), '{key}')]\
                            or @title='{key}' or @class='{key}' or descendant::div[contains(text(), '{key}')]\
                            or ancestor::div[contains(text(), '{key}')]]")
                    search_key = (By.XPATH, xpath)
                elif by_type == "LABEL":
                    xpath = f"//label[text() = '{key}']/following-sibling::div//input"
                    search_key = (By.XPATH, xpath)
                elif by_type == "TEXT":
                    xpath = f"//input[contains(text(), '{key}') or contains(@placeholder, '{key}')]"                    
                    search_key = (By.XPATH, xpath)
                else:
                    search_key = (by_type, key)

                element = WebDriverWait(self.browser, timeout).until(
                    EC.presence_of_all_elements_located(search_key)
                )

                if len(element) > 0:
                    start_time = time.time()
                    while not element[0].is_displayed() and time.time() - start_time < timeout:
                        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    element[0].clear()
                    element[0].send_keys(value)
                else:
                    result = False
                    msg = "Failed to appear or click on element within the specified timeout"

            elif action == "upload":
                search_key = (by_type, key)
                element = WebDriverWait(self.browser, 10).until(
                    EC.presence_of_all_elements_located(search_key)
                )
                element[0].send_keys(os.path.dirname(os.path.abspath(__file__)) + value)
            elif action == "press":
                if key.upper() == "GLOBAL":
                    actionchains.send_keys(getattr(Keys, value.upper(), value))
                    actionchains.perform()
            elif action == "expect":
                if by_type == "title":
                    result = EC.title_contains(key)
                    if not result:
                        msg = "Failed to appear title"
                elif by_type == "text":
                    result = EC.text_to_be_present_in_element((By.XPATH, value), key)
                    if not result:
                        msg = "Failed to appear text"
                elif by_type == "CONTAIN":
                    xpath = f"//{self.elem_dict[value]}[.//span[contains(text(), '{key}')] or contains(text(), '{key}') or @title='{key}' or @class='{key}']"           
                    result = EC.visibility_of_element_located((By.XPATH, xpath))
                    if not result:
                        msg = "Failed to appear element"
                else:
                    result = EC.visibility_of_element_located((by_type, key))
                    if not result:
                        msg = "Failed to appear element"
            else:
                pass
            return True, "pass"
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            msg = f"Failed to do {action} {key} {value}"
        
        return False, msg
      
    def test_execute(self):
        for testcase in self.test_config:
            print(testcase["name"])
            self.browser.get(testcase['url'])
            if not EC.title_contains(testcase["title"]):
                self.test_report.update({testcase["name"]: "Failed to appear title"})
                continue

            actionchains = ActionChains(self.browser)
            for index, step in enumerate(testcase['test_steps']):
                result, msg = True, "pass"
                print(step)
                for action, step_config in step.items():
                    if action.split("_")[0] == "iteration":
                        iteration_count = int(action.split("_")[1])
                        index += 1
                        index_length = len(step_config)
                        for i in range(iteration_count):
                            for j, loop_step in enumerate(step_config):
                                testcase['test_steps'].insert(index + index_length*i + j, loop_step)
                        index -= 1
                    elif action.split("_")[0] == "try":
                        try:
                            self.execute_common_logic(step_config, action.split("_")[1], actionchains, timeout=5)
                        except:
                            pass
                    elif action.split("_")[0] == "wait":
                        if action.split("_")[1].isnumeric():
                            sleep(int(action.split("_")[1]))
                            print("wait for " + action.split("_")[1] + " seconds")
                            result, msg = self.execute_common_logic(step_config, action.split("_")[2], actionchains)
                        else:
                            sleep(5)
                            result, msg = self.execute_common_logic(step_config, action.split("_")[1], actionchains)
                    else:
                        result, msg = self.execute_common_logic(step_config, action, actionchains)
        
                self.test_report.update({testcase["name"]: msg})
                if not result:
                    break

    def make_report(self):
        print("make report")
        report_path = os.path.dirname(os.path.abspath(__file__)) + f"/report/{self.time_stamp}_report.txt"
        with open(report_path, "w") as file:
            for key, value in self.test_report.items():
                print(f"{key}: {value}")
                file.write(f"{key}: {value}\n")

    def tearDown(self):
        self.make_report()
                
if __name__ == '__main__':
    unittest.main(verbosity=2)
