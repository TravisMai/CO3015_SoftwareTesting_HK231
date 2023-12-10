import unittest
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

results = []

class AddQuizLv0(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()

    def tearDown(self):
        self.driver.quit()

    def login(self, username, password, link):
        self.driver.get(link)
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "loginbtn").click()

    def is_exist(self, css_selector):
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return False
        return True
    
    def navigate_to_my_course(self):
        self.driver.find_element(By.CSS_SELECTOR, "a[href='https://school.moodledemo.net/my/courses.php']").click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='https://school.moodledemo.net/course/view.php?id=27']"))
        ).click()

        self.driver.find_element(By.NAME, "setmode").click()

    # Method to navigate to Site administration -> Courses -> Manage courses and categories
    def navigate_to_manage_courses(self):
        self.driver.find_element(By.LINK_TEXT, "Site administration").click()
        self.driver.find_element(By.LINK_TEXT, "Courses").click()
        self.driver.find_element(By.LINK_TEXT, "Manage courses and categories").click()

    def go_to_add_quiz(self):
        self.navigate_to_my_course()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#coursecontentcollapse0 .activity-add-text"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Add a new Quiz']"))
        ).click()

    def add_quiz(self, name):
        self.driver.find_element(By.NAME, "name").send_keys(name)
        self.driver.find_element(By.NAME, "submitbutton").click()

    def test_01(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.go_to_add_quiz()
        self.add_quiz('Quiz01')

        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'Quiz01':
                results.append({"Test Case": "01", "Result": "Passed"})
                return
        
        results.append({"Test Case": "01", "Result": "Failed"})

    def test_02(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.go_to_add_quiz()
        self.add_quiz('')

        if self.driver.find_element(By.CSS_SELECTOR, '#id_error_name'):
            results.append({"Test Case": "02", "Result": "Passed"})
        else: results.append({"Test Case": "02", "Result": "Failed"})
        
    def test_03(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.go_to_add_quiz()
        self.add_quiz('Q')

        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'Q':
                results.append({"Test Case": "03", "Result": "Passed"})
                return
        
        results.append({"Test Case": "03", "Result": "Failed"})

    def test_04(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.go_to_add_quiz()
        self.add_quiz('QuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuizna')
        
        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'QuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuizna':
                results.append({"Test Case": "04", "Result": "Passed"})
                return
        
        results.append({"Test Case": "04", "Result": "Failed"})

    def test_05(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.go_to_add_quiz()
        self.add_quiz('QuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznam')
        
        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'QuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznam':
                results.append({"Test Case": "05", "Result": "Passed"})
                return
        
        results.append({"Test Case": "05", "Result": "Failed"})

    def test_06(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.go_to_add_quiz()
        self.add_quiz('QuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuiznameQuizname')
        
        if self.driver.find_element(By.CSS_SELECTOR, '#id_error_name'):
            results.append({"Test Case": "06", "Result": "Passed"})
        else: results.append({"Test Case": "06", "Result": "Failed"})

    def test_07(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.driver.find_element(By.LINK_TEXT, "Dashboard").click()
        self.driver.find_element(By.LINK_TEXT, "Mount Orange Community").click()
        self.driver.find_element(By.LINK_TEXT, "Parents and Citizens Council").click()
        self.driver.find_element(By.NAME, "setmode").click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#coursecontentcollapse0 .activity-add-text"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Add a new Quiz']"))
        ).click()

        self.add_quiz('This is a Quiz')

        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'This is a Quiz':
                results.append({"Test Case": "07", "Result": "Passed"})
                return
        
        results.append({"Test Case": "07", "Result": "Failed"})

    def test_08(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.navigate_to_manage_courses()

        course_list = self.driver.find_element(By.CSS_SELECTOR, 'ul.course-list')
        course_list.find_element(By.CSS_SELECTOR, 'li.listitem.listitem-course').click()

        self.driver.find_element(By.LINK_TEXT, "View").click()

        self.driver.find_element(By.NAME, "setmode").click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#coursecontentcollapse0 .activity-add-text"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[title='Add a new Quiz']"))
        ).click()

        self.add_quiz('This is a Quiz 02')

        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'This is a Quiz 02':
                results.append({"Test Case": "08", "Result": "Passed"})
                return
        
        results.append({"Test Case": "08", "Result": "Failed"})
    
    def test_results(self):
        # Export results to a DataFrame
        df = pd.DataFrame(results)
        print(df)
        df.to_csv("add_quiz_test_results.csv", index=False)

if __name__ == "__main__":
    unittest.main()

    