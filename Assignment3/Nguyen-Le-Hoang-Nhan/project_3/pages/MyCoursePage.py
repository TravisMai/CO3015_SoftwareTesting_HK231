from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlsplit
import project_3.pages.CoursePage

from project_3.utils.exceptions import IllegalStateError


class MyCoursePage:
    loading_icon_by = (
        By.XPATH,
        '//*[@id="page-container-1"]//span[@class="loading-icon"]',
    )

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        if urlsplit(driver.current_url).path != "/my/courses.php":
            raise IllegalStateError(
                f"This is not My Course page, current page is: {driver.current_url}"
            )

        WebDriverWait(self.driver, 20).until_not(
            EC.presence_of_element_located(self.loading_icon_by)
        )  # wait for all course to load

    def go_to_course(self, course_id: int) -> project_3.pages.CoursePage.CoursePage:
        course_link = self.driver.find_element(
            By.XPATH, f'//a[contains(@href, "course/view.php?id={course_id}")]'
        )
        course_link.click()

        return project_3.pages.CoursePage.CoursePage(self.driver)
