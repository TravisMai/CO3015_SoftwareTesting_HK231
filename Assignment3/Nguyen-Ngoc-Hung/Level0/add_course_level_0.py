import unittest
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

results = []

class AddCourseLv0(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()

    def tearDown(self):
        self.driver.quit()

    # Create the login method
    def login(self, username, password, link):
        self.driver.get(link)
        self.driver.find_element(By.LINK_TEXT, "Log in").click()
        self.driver.find_element(By.ID, "username").send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "loginbtn").click()

    # Check existence of an element
    def is_exist(self, css_selector):
        try:
            self.driver.find_element(By.CSS_SELECTOR, css_selector)
        except NoSuchElementException:
            return False
        return True

    # Method to navigate to Site administration -> Courses -> Manage courses and categories
    def navigate_to_manage_courses(self):
        self.driver.find_element(By.LINK_TEXT, "Site administration").click()
        self.driver.find_element(By.LINK_TEXT, "Courses").click()
        self.driver.find_element(By.LINK_TEXT, "Manage courses and categories").click()

    # Method to navigate to Site administration -> Courses -> Add a new course
    def navigate_to_add_course_directly(self):
        self.driver.find_element(By.LINK_TEXT, "Site administration").click()
        self.driver.find_element(By.LINK_TEXT, "Courses").click()
        self.driver.find_element(By.LINK_TEXT, "Add a new course").click()

    # Method to go to Site administration -> Courses -> Add a category
    def navigate_to_add_category(self):
        self.driver.find_element(By.LINK_TEXT, "Site administration").click()
        self.driver.find_element(By.LINK_TEXT, "Courses").click()
        self.driver.find_element(By.LINK_TEXT, "Add a category").click()

    # Method to click Create new course, fill in fullname and shortname, then click Save and Display
    def add_course_with_required_info(self, course_name, course_shortname):
        self.navigate_to_manage_courses()
        self.driver.find_element(By.LINK_TEXT, "Create new course").click()
        self.driver.find_element(By.ID, "id_fullname").send_keys(course_name)
        self.driver.find_element(By.ID, "id_shortname").send_keys(course_shortname)
        self.driver.find_element(By.NAME, "saveanddisplay").click()

    # Method to fill in fullname and shortname, then click Save and Display
    def add_course_with_required_info_directly(self,course_name, course_shortname):
        self.navigate_to_add_course_directly()
        self.driver.find_element(By.ID, "id_fullname").send_keys(course_name)
        self.driver.find_element(By.ID, "id_shortname").send_keys(course_shortname)
        self.driver.find_element(By.NAME, "saveanddisplay").click()

    # Method to add new category then add a course of that category
    def add_course_after_creating_category(self, category_name, course_name, course_shortname):
        self.navigate_to_add_category()
        self.driver.find_element(By.ID, "id_name").send_keys(category_name)
        self.driver.find_element(By.NAME, "submitbutton").click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".categoryname"))
        )
        self.driver.find_element(By.LINK_TEXT, "Create new course").click()
        self.driver.find_element(By.ID, "id_fullname").send_keys(course_name)
        self.driver.find_element(By.ID, "id_shortname").send_keys(course_shortname)
        self.driver.find_element(By.NAME, "saveanddisplay").click()

    # Method to leave everything blank
    def add_course_without_required_info(self):
        self.navigate_to_manage_courses()
        self.driver.find_element(By.LINK_TEXT, "Create new course").click()
        self.driver.find_element(By.NAME, "saveanddisplay").click()

    # Method to add course by upload a file
    def add_course_by_uploading_csv(self, csv_filename):
        csv_path = os.path.abspath(os.path.join(os.getcwd(), csv_filename))
    
        self.driver.find_element(By.LINK_TEXT, "Site administration").click()
        self.driver.find_element(By.CSS_SELECTOR, "a[href='#linkcourses']").click()
        self.driver.find_element(By.LINK_TEXT, "Upload courses").click()
        
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "coursefilechoose"))
        ).click()

        self.driver.find_element(By.LINK_TEXT, "Upload a file").click()

        # Find the file input element and send the absolute path of the CSV file
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "repo_upload_file"))
        )
        file_input.send_keys(csv_path)
        
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fp-upload-btn"))
        ).click()

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "submitbutton"))
        ).click()
    
    # Successfully add a new course with all required information
    def test_01(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.add_course_with_required_info('Test Course', 'TC001')

        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'Test Course':
                results.append({"Test Case": "01", "Result": "Passed"})
                return

        results.append({"Test Case": "01", "Result": "Failed"})

    # Successfully add a new course with all required information using Course -> Add a new course
    def test_02(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.add_course_with_required_info_directly('Test Course 02', 'TC002')

        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'Test Course 02':
                results.append({"Test Case": "02", "Result": "Passed"})
                return
        
        results.append({"Test Case": "02", "Result": "Failed"})

    # Successfully add a new course with all required information after create a new category
    def test_03(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.add_course_after_creating_category('Test category', 'Test Course 03', 'TC03')

        if(self.is_exist('h1.h2')):
            if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == 'Test Course 03':
                results.append({"Test Case": "03", "Result": "Passed"})
                return
        
        results.append({"Test Case": "03", "Result": "Failed"})

    # Add a new course without filling any required information
    def test_04(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        self.add_course_without_required_info()
        
        fullname_error = '#id_error_fullname'
        shortname_error = '#id_error_shortname'

        if self.is_exist(fullname_error) or self.is_exist(shortname_error):
            results.append({"Test Case": "04", "Result": "Passed"})
        else: results.append({"Test Case": "04", "Result": "Failed"})
    
    def test_05(self):
        self.login('admin', 'sandbox', 'https://sandbox.moodledemo.net/')
        self.add_course_by_uploading_csv('files/testcourse.csv')

        if self.is_exist('i.icon.fa.fa-check.text-success.fa-fw'):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#id_submitbutton"))
            ).click()
            results.append({"Test Case": "05", "Result": "Passed"})
        else:
            results.append({"Test Case": "05", "Result": "Failed"})
    
    def test_06(self):
        self.login('admin', 'sandbox', 'https://sandbox.moodledemo.net/')
        self.add_course_by_uploading_csv('files/testcourse_missing_value.txt')

        if self.is_exist('i.icon.fa.fa-times.text-danger.fa-fw'):
            results.append({"Test Case": "06", "Result": "Passed"})
        else: results.append({"Test Case": "06", "Result": "Failed"})

    def test_07(self):
        self.login('admin', 'sandbox', 'https://sandbox.moodledemo.net/')
        self.add_course_by_uploading_csv('files/testcourse.txt')

        if self.is_exist('i.icon.fa.fa-check.text-success.fa-fw'):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#id_submitbutton"))
            ).click()
            results.append({"Test Case": "07", "Result": "Passed"})
        else: results.append({"Test Case": "07", "Result": "Failed"})      

    def test_08(self):
        self.login('admin', 'sandbox', 'https://sandbox.moodledemo.net/')
        self.add_course_by_uploading_csv('files/testcourse.pdf')

        if not self.is_exist('i.icon.fa.fa-times.text-danger.fa-fw'):
            results.append({"Test Case": "08", "Result": "Passed"})
        else: results.append({"Test Case": "08", "Result": "Failed"})

    def test_results(self):
        # Export results to a DataFrame
        df = pd.DataFrame(results)
        print(df)
        df.to_csv("add_course_test_results.csv", index=False)

if __name__ == "__main__":
    unittest.main()

    