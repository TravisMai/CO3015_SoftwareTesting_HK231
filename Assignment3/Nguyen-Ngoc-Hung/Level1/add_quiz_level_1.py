import unittest
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

results = []

class AddQuizLv1(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Edge()

    def tearDown(self):
        self.driver.quit()

    def read_test_data(self, csv_filename):
        csv_path = os.path.abspath(os.path.join(os.getcwd(), csv_filename))
        test_data = pd.read_csv(csv_path)
        return test_data

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

    def test_add_quiz(self):
        self.login('manager', 'moodle', "https://school.moodledemo.net")
        test_data = self.read_test_data('test_data/test_data_add_quiz.csv')
        self.driver.find_element(By.NAME, "setmode").click()

        count = 1

        for index, row in test_data.iterrows():
            quizname = row['quizname']

            self.go_to_add_quiz()
            self.add_quiz(quizname)

            tf = "Test add quiz " + str(count)
            count += 1

            if(self.is_exist('h1.h2')):
                if self.driver.find_element(By.CSS_SELECTOR, 'h1.h2').text == quizname:
                    results.append({"Test function": tf, "Status": "Successful", "Expected": row['expected']})
                else: results.append({"Test function": tf, "Status": "Fail", "Expected": row['expected']})

    
    def show_results(self):
        # Export results to a DataFrame
        df = pd.DataFrame(results)
        print(df)
        df.to_csv("add_quiz_test_results.csv", index=False)
        

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(AddQuizLv1)
    unittest.TextTestRunner().run(suite)

    AddQuizLv1().show_results()

    