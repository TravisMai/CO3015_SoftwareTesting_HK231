from typing import Any, Self
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from urllib.parse import urlsplit
import project_3.pages.DiscussionPage
import project_3.pages.AdvanceAddDiscussionPage

from project_3.utils.exceptions import IllegalStateError


class ForumPage:
    add_discussion_topic_form_button_by = (By.XPATH, '//a[@href="#collapseAddForm"]')
    add_discussion_topic_form_area_by = (By.ID, "collapseAddForm")
    subject_field_by = (By.ID, "id_subject")
    message_field_iframe_by = (By.ID, "id_message_ifr")
    message_field_body_by = (By.TAG_NAME, "body")

    post_to_forum_button_by = (By.ID, "id_submitbutton")
    advance_add_discussion_button_by = (By.ID, "id_advancedadddiscussion")

    latest_discussion_by = (
        By.XPATH,
        "//table[contains(@class, 'discussion-list')]/tbody/tr[1]//th//a",
    )

    subject_error_by = (By.XPATH, "//div[@id='id_error_subject']")
    content_error_by = (By.XPATH, "//div[@id='id_error_message']")

    state = {"add_form_openned": False}

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        if urlsplit(driver.current_url).path != "/mod/forum/view.php":
            raise IllegalStateError(
                f"This is not a Forum page, current page is: {driver.current_url}"
            )

    def get_subject_error(self) -> str:
        return self.driver.find_element(*self.subject_error_by).text

    def get_content_error(self):
        return self.driver.find_element(*self.content_error_by).text

    def _open_add_discussion_form(self):
        if not self.state["add_form_openned"]:
            WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(self.add_discussion_topic_form_button_by)
            )
            open_add_discussion_topic_form_button = self.driver.find_element(
                *self.add_discussion_topic_form_button_by
            )
            open_add_discussion_topic_form_button.click()

            WebDriverWait(self.driver, 20).until(
                EC.text_to_be_present_in_element_attribute(
                    self.add_discussion_topic_form_area_by, "class", "show"
                ),
                "Add discussion area field form does not open on time",
            )

    # def _close_add_discussion_form(self):
    #     if self.state["add_form_openned"]:
    #         open_add_discussion_topic_form_button = self.driver.find_element(
    #             *self.add_discussion_topic_form_button_by
    #         )
    #         open_add_discussion_topic_form_button.click()

    #         WebDriverWait(self.driver, 3).until_not(
    #             EC.text_to_be_present_in_element_attribute(
    #                 self.add_discussion_topic_form_area_by, "class", "show"
    #             ),
    #             "Add discussion area field form does not close on time",
    #         )

    def post_discussion(self, subject: str, content: str) -> Self:
        self._open_add_discussion_form()

        subject_field = self.driver.find_element(*self.subject_field_by)
        subject_field.send_keys(subject)

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(self.message_field_iframe_by),
            "Cannot find the content frame",
        )

        content_field_iframe = self.driver.find_element(*self.message_field_iframe_by)
        self.driver.switch_to.frame(content_field_iframe)

        content_field = self.driver.find_element(*self.message_field_body_by)
        content_field.click()
        content_field.send_keys(content)

        self.driver.switch_to.default_content()

        post_to_forum_button = self.driver.find_element(*self.post_to_forum_button_by)
        post_to_forum_button.click()

        return ForumPage(self.driver)

    # def post_invalid_discussion(self, subject: str, content: str):

    def go_to_latest_discussion(self) -> project_3.pages.DiscussionPage.DiscussionPage:
        latest_discussion_link = self.driver.find_element(*self.latest_discussion_by)
        latest_discussion_link.click()

        return project_3.pages.DiscussionPage.DiscussionPage(self.driver)

    def go_to_advance_add_page(
        self,
    ) -> project_3.pages.AdvanceAddDiscussionPage.AdvanceAddDiscussionPage:
        self._open_add_discussion_form()

        self.driver.find_element(*self.advance_add_discussion_button_by).click()

        return project_3.pages.AdvanceAddDiscussionPage.AdvanceAddDiscussionPage(
            self.driver
        )
