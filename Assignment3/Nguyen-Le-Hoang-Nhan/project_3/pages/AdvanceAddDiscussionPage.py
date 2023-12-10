from sys import platform
from typing import Self
import time

import project_3.pages.ForumPage

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException

from urllib.parse import urlsplit

from project_3.utils.exceptions import IllegalStateError

FILE_CONTAINER_BY = (
    By.XPATH,
    '//div[contains(@class, "filemanager")]/div[contains(@class, "fp-navbar")]/div[contains(@class, "filemanager-toolbar")]/div[contains(@class, "fp-toolbar")]/div[@class="fp-btn-add"]/a[@role="button"]',
)
FILE_LOADING_BY = (By.XPATH, '//div[contains(@class, "filemanager-loading")]')
FILE_UPLOAD_BUTTON_BY = (By.XPATH, '//span[contains(., "Upload a file")]')
FILE_INPUT_FIELD_BY = (
    By.XPATH,
    "//input[@type='file' and @name='repo_upload_file']",
)
FILE_INPUT_LOADING_INDICATOR_BY = (
    By.XPATH,
    '//div[contains(@class, "fp-content-loading")]',
)
UPLOAD_FILE_BUTTON_BY = (By.XPATH, "//button[@class='fp-upload-btn btn-primary btn']")

PATH_SEP = "\\" if platform == "win32" else "/"


class AdvanceAddDiscussionPage:
    add_discussion_topic_form_button_by = (By.XPATH, '//a[@href="#collapseAddForm"]')
    add_discussion_topic_form_area_by = (By.ID, "collapseAddForm")
    subject_field_by = (By.ID, "id_subject")
    message_field_iframe_by = (By.ID, "id_message_ifr")
    message_field_body_by = (By.TAG_NAME, "body")

    file_container_by = (
        By.XPATH,
        '//div[contains(@class, "filemanager")]/div[contains(@class, "fp-navbar")]/div[contains(@class, "filemanager-toolbar")]/div[contains(@class, "fp-toolbar")]/div[@class="fp-btn-add"]/a[@role="button"]',
    )
    file_loading_by = (By.XPATH, '//div[contains(@class, "filemanager-loading")]')
    file_upload_button_by = (By.XPATH, '//span[contains(., "Upload a file")]')
    file_input_field_by = (
        By.XPATH,
        "//input[@type='file' and @name='repo_upload_file']",
    )
    file_input_loading_indicator_by = (
        By.XPATH,
        '//div[contains(@class, "fp-content-loading")]',
    )
    upload_file_button_by = (By.XPATH, "//button[contains(., 'Upload this file')]")

    post_to_forum_button_by = (By.ID, "id_submitbutton")
    subject_error_by = (By.XPATH, "//div[@id='id_error_subject']")
    content_error_by = (By.XPATH, "//div[@id='id_error_message']")

    upload_file_error_debug_code_by = (
        By.XPATH,
        '//div[@class="moodle-exception-param param-debuginfo"][2]',
    )

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        if urlsplit(driver.current_url).path != "/mod/forum/post.php":
            raise IllegalStateError(
                f"This is not a {__name__} page, current page is: {driver.current_url}"
            )

    def get_subject_error(self) -> str:
        return self.driver.find_element(*self.subject_error_by).text

    def get_content_error(self) -> str:
        return self.driver.find_element(*self.content_error_by).text

    def get_file_upload_error(self) -> str:
        WebDriverWait(self.driver, 600).until(
            EC.presence_of_element_located(self.upload_file_error_debug_code_by)
        )
        return (
            self.driver.find_element(*self.upload_file_error_debug_code_by)
            .text.split(":")[-1]
            .lstrip()
        )

    def post_valid_discussion(
        self, subject: str, content: str, file_path: str = None
    ) -> "project_3.pages.ForumPage.ForumPage":
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

        if file_path:
            WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element_located(self.file_loading_by)
            )
            self.add_file_to_attachement_list(file_path)

        post_to_forum_button = self.driver.find_element(*self.post_to_forum_button_by)
        post_to_forum_button.click()

        return project_3.pages.ForumPage.ForumPage(self.driver)

    def post_invalid_discussion(
        self, subject: str, content: str, file_path: str = None
    ) -> Self:
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

        if file_path:
            WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element_located(self.file_loading_by)
            )
            self.add_file_to_attachement_list(file_path)

        post_to_forum_button = self.driver.find_element(*self.post_to_forum_button_by)
        post_to_forum_button.click()

        return self

    def post_large_file_to_discussion(
        self, subject: str, content: str, file_path: str = None
    ) -> Self:
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

        if file_path:
            WebDriverWait(self.driver, 20).until(
                EC.invisibility_of_element_located(self.file_loading_by)
            )
            self._upload_file(file_path)

        return self

    def add_file_to_attachement_list(self, file_path: str):
        self.driver.find_element(*FILE_CONTAINER_BY).click()

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(FILE_UPLOAD_BUTTON_BY)
        )
        self.driver.find_element(*FILE_UPLOAD_BUTTON_BY).click()

        WebDriverWait(self.driver, 20).until_not(
            EC.visibility_of_element_located(FILE_INPUT_LOADING_INDICATOR_BY)
        )

        self.driver.find_element(*FILE_UPLOAD_BUTTON_BY).click()

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(FILE_INPUT_FIELD_BY)
        )

        retry_choose_file = 5
        while retry_choose_file:
            self.driver.find_element(*FILE_INPUT_FIELD_BY).send_keys(file_path)
            value = self.driver.execute_script(
                "return arguments[0].value",
                self.driver.find_element(*FILE_INPUT_FIELD_BY),
            )
            if (
                isinstance(value, str)
                and value.split("\\")[-1] == file_path.split(PATH_SEP)[-1]
            ):
                break
            retry_choose_file = retry_choose_file - 1
            time.sleep(0.5)

        if retry_choose_file == 0:
            raise IllegalStateError("Cannot choose file to upload")

        retry_choose_file = 5
        while retry_choose_file:
            try:
                self.driver.find_element(*UPLOAD_FILE_BUTTON_BY).click()
                break
            except StaleElementReferenceException:
                retry_choose_file = retry_choose_file - 1
                time.sleep(0.5)

        if retry_choose_file == 0:
            raise IllegalStateError(
                "Cannot click the upload file button because of StaleElementReferenceExceptions"
            )

    def _upload_file(self, file_path: str):
        self.driver.find_element(*self.file_container_by).click()

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.file_upload_button_by)
        )
        self.driver.find_element(*self.file_upload_button_by).click()

        WebDriverWait(self.driver, 20).until_not(
            EC.visibility_of_element_located(self.file_input_loading_indicator_by)
        )

        self.driver.find_element(*self.file_upload_button_by).click()

        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(self.file_input_field_by)
        )
        self.driver.find_element(*self.file_input_field_by).send_keys(file_path)

        self.driver.find_element(*self.upload_file_button_by).click()

        # WebDriverWait(self.driver, 20).until_not(
        #     EC.visibility_of_element_located(self.file_upload_button_by)
        # )
