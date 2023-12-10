from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from urllib.parse import urlsplit
import project_3.pages.MyCoursePage

from project_3.utils.exceptions import IllegalStateError


class DashboardPage:
    my_course_link_by = (By.LINK_TEXT, "My courses")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        if urlsplit(driver.current_url).path != "/my/":
            raise IllegalStateError(
                f"This is not Dash Board, current page is: {driver.current_url}"
            )

    def go_to_my_course(self) -> project_3.pages.MyCoursePage.MyCoursePage:
        self.driver.find_element(*self.my_course_link_by).click()
        return project_3.pages.MyCoursePage.MyCoursePage(self.driver)
