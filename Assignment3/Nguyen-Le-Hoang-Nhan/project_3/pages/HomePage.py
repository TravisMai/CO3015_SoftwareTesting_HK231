from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from urllib.parse import urlsplit

from project_3.utils.exceptions import IllegalStateError
import project_3.pages.SignInPage


class HomePage:
    login_link_by = (By.LINK_TEXT, "Log in")

    def __init__(self, driver: WebDriver, logged_in=False) -> None:
        self.driver = driver
        self.logged_in = logged_in
        if urlsplit(driver.current_url).path != "/":
            raise IllegalStateError(
                f"This is not Home Page, current page is: {driver.current_url}"
            )

    def go_to_signin(self) -> project_3.pages.SignInPage.SignInPage:
        if self.logged_in:
            raise IllegalStateError(f"User is already logged in, cannot logged in")

        self.driver.find_element(*self.login_link_by).click()
        return project_3.pages.SignInPage.SignInPage(self.driver)
