from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from urllib.parse import urlsplit, unquote

from project_3.utils.exceptions import IllegalStateError


class DiscussionPage:
    discussion_topic_by = (
        By.XPATH,
        "//div[@role='main']/div/article/div/div/header/div[2]/h3",
    )
    discussion_original_content_by = (
        By.XPATH,
        "//div[@role='main']/div/article/div/div/div/div[2]/div[@class='post-content-container']/p",
    )

    attachment_files_by = (
        By.XPATH,
        '//div[@role="main"]/div/article/div/div/div/div[2]/*[not(contains(@class, "post-content-container"))]/a[@href]',
    )

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

        if urlsplit(driver.current_url).path != "/mod/forum/discuss.php":
            raise IllegalStateError(
                f"This is not a Discussion page, current page is: {driver.current_url}"
            )

    def get_discussion_subject(self) -> str:
        return self.driver.find_element(*self.discussion_topic_by).text

    def get_discussion_content(self) -> str:
        return self.driver.find_element(*self.discussion_original_content_by).text

    def get_discussion_attachment_file_list(self) -> list[str]:
        attachment_files_link = self.driver.find_elements(*self.attachment_files_by)
        attachment_files_name = [
            unquote(urlsplit(link.get_attribute("href")).path.split("/")[-1])
            for link in attachment_files_link
        ]
        return attachment_files_name
