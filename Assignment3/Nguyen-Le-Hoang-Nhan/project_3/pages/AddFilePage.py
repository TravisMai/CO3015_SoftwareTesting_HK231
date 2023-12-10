import time
from sys import platform
from typing import Self
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from urllib.parse import urlsplit

from project_3.utils.exceptions import IllegalStateError
import project_3.pages.CoursePage

NAME_FIELD_BY = (By.ID, "id_name")
DESCRIPTION_FIELD_FRAME_BY = (By.ID, "id_introeditor_ifr")
DESCRIPTION_FIELD_FRAME_BODY_BY = (By.ID, "tinymce")
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
FILE_ERROR_BY = (By.ID, "id_error_files")
NAME_ERROR_BY = (By.ID, "id_error_name")

SAVE_AND_RETURN_TO_COURSE_BUTTON_BY = (By.ID, "id_submitbutton2")

PATH_SEP = "\\" if platform == "win32" else "/"


class AddFilePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        if urlsplit(driver.current_url).path != "/course/modedit.php":
            raise IllegalStateError(
                f"This is not an {__class__}, current page is: {driver.current_url}"
            )

    def fill_in_name(self, file_resource_name: str) -> Self:
        self.driver.find_element(*NAME_FIELD_BY).send_keys(file_resource_name)
        return self

    def fill_in_description(self, file_resouce_description: str) -> Self:
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located(DESCRIPTION_FIELD_FRAME_BY)
        )
        self.driver.switch_to.frame(
            self.driver.find_element(*DESCRIPTION_FIELD_FRAME_BY)
        )
        self.driver.find_element(*DESCRIPTION_FIELD_FRAME_BODY_BY).click()
        if platform == "darwin":
            self.driver.find_element(*DESCRIPTION_FIELD_FRAME_BODY_BY).send_keys(
                Keys.COMMAND + "a"
            )
            self.driver.find_element(*DESCRIPTION_FIELD_FRAME_BODY_BY).send_keys(
                Keys.BACKSPACE
            )
        else:
            self.driver.find_element(*DESCRIPTION_FIELD_FRAME_BODY_BY).send_keys(
                Keys.CONTROL + "a"
            )
            self.driver.find_element(*DESCRIPTION_FIELD_FRAME_BODY_BY).send_keys(
                Keys.BACKSPACE
            )

        self.driver.find_element(*DESCRIPTION_FIELD_FRAME_BODY_BY).send_keys(
            file_resouce_description
        )
        self.driver.switch_to.default_content()
        return self

    def toggle_display_description_on_course_page(self) -> Self:
        ...

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
            try:
                self.driver.find_element(*FILE_INPUT_FIELD_BY).send_keys(file_path)

            except StaleElementReferenceException:
                retry_choose_file = retry_choose_file - 1
                time.sleep(0.5)
                continue

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

    def submit_resource(self) -> "project_3.pages.CoursePage.CoursePage":
        self.driver.find_element(*SAVE_AND_RETURN_TO_COURSE_BUTTON_BY).click()
        return project_3.pages.CoursePage.CoursePage(self.driver)

    def submit_invalid_resource(self) -> Self:
        self.driver.find_element(*SAVE_AND_RETURN_TO_COURSE_BUTTON_BY).click()
        return self

    def get_file_error(self) -> str:
        return self.driver.find_element(*FILE_ERROR_BY).text.lstrip().rstrip()

    def get_name_error(self) -> str:
        return self.driver.find_element(*NAME_ERROR_BY).text.lstrip().rstrip()
