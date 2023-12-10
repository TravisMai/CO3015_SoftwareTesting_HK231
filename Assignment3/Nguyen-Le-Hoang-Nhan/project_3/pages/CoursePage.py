import time
from typing import Any, Self
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import urlsplit

from project_3.utils.exceptions import IllegalStateError
import project_3.pages.ForumPage
import project_3.pages.AddFilePage

add_activity_icon_by = (By.XPATH, '//img[@class="icon activityicon "]')

add_resource_button_by = (By.XPATH, '//span[text()="Add an activity or resource"]')
file_resource_button_by = (By.XPATH, '//div[text()="File"]')

loading_icon_by = (
    By.XPATH,
    '//*[@id="page-container-1"]//span[@class="loading-icon"]',
)
edit_mode_toggler_by = (
    By.XPATH,
    '//div[@class="custom-control custom-switch"]/input',
)

forum_link_by = lambda forum_id: (
    By.XPATH,
    f'//a[contains(@href, "mod/forum/view.php?id={forum_id}")]',
)

resource_link_by = (
    By.XPATH,
    '//li[contains(@class, "resource modtype_resource")]//div[@class="activityname"]/a',
)

edit_resource_link_by = lambda resource_name: (
    By.XPATH,
    f'//li[contains(@class, "resource modtype_resource") and .//span[@class="instancename" and normalize-space(.) = "{resource_name}"]]',
)

action_menu_by = (
    By.XPATH,
    './/div[contains(@class, "activity-actions")]//a[@href="#"]',
)


# class DocumentSettleCondition:
#     def __init__(self, condition, settle_time_in_millis) -> None:
#         self.condition = condition
#         self.settle_time_in_millis = settle_time_in_millis
#         self.last_complete = 0
#         self.last_url = ""

#     def __call__(self, driver: WebDriver) -> Any:
#         current_url = driver.current_url
#         ready_state: str = driver.execute_script("return document.readyState")
#         ready_state = ready_state.lower()
#         if ready_state != "complete":
#             self.last_complete = 0
#             return None


class CoursePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        WebDriverWait(self.driver, 20).until(EC.url_contains("view.php"))

        if urlsplit(driver.current_url).path != "/course/view.php":
            raise IllegalStateError(
                f"This is not a Course page, current page is: {driver.current_url}"
            )

    def go_to_forum(self, forum_id: int) -> project_3.pages.ForumPage.ForumPage:
        forum_link = self.driver.find_element(*forum_link_by(forum_id))
        forum_link.click()

        return project_3.pages.ForumPage.ForumPage(self.driver)

    def toggle_edit_mode(self) -> Self:
        edit_mode_toggler = self.driver.find_element(*edit_mode_toggler_by)
        edit_mode_toggler.click()

        return self

    def go_to_add_file_page(self) -> project_3.pages.AddFilePage.AddFilePage:
        add_activity_button = self.driver.find_element(*add_resource_button_by)
        add_activity_button.click()
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(add_activity_icon_by)
        )
        self.driver.find_element(*file_resource_button_by).click()
        return project_3.pages.AddFilePage.AddFilePage(self.driver)

    def get_list_of_file_resource(self) -> list[tuple[str, str]]:
        resource_links = self.driver.find_elements(*resource_link_by)
        print(resource_links)
        resource_names = [
            resource_link.find_element(By.XPATH, ".//span").text.lstrip().rstrip()
            for resource_link in resource_links
        ]
        resource_link_hrefs = [
            resource_link.get_attribute("href") for resource_link in resource_links
        ]
        return list(zip(resource_names, resource_link_hrefs))

    # def delete_resource_with_name(self, resource_name: str):
    #     WebDriverWait(self.driver, 20).until(
    #         EC.text_to_be_present_in_element((By.TAG_NAME, "body"), resource_name)
    #     )
    #     resource_list_item = self.driver.find_element(
    #         *edit_resource_link_by(resource_name)
    #     )
    #     resource_list_item.find_element(*action_menu_by).click()
