from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from urllib.parse import urlsplit

from project_3.utils.exceptions import IllegalStateError
import project_3.pages.DashboardPage


class SignInPage:
    username_by = (By.ID, "username")
    password_by = (By.ID, "password")
    login_button_by = (By.ID, "loginbtn")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        if urlsplit(driver.current_url).path != "/login/index.php":
            raise IllegalStateError(
                f"This is not Sign In Page, current page is: {driver.current_url}"
            )

    def login_valid_user(
        self, username: str, password: str
    ) -> project_3.pages.DashboardPage.DashboardPage:
        self.driver.find_element(*self.username_by).send_keys(username)
        self.driver.find_element(*self.password_by).send_keys(password)
        self.driver.find_element(*self.login_button_by).click()

        return project_3.pages.DashboardPage.DashboardPage(self.driver)
