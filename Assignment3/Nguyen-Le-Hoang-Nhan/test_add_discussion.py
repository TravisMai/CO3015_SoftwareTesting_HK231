from selenium import webdriver

from selenium.webdriver.firefox.options import Options as FirefoxOptions

import pytest
from pytest import fixture
import project_3.pages.CoursePage

from project_3.pages.HomePage import HomePage
from project_3.utils.config import get_test_config, get_tests
from project_3.utils.gen_file import gen_file_in_path


class TestAddDiscussion:
    @fixture(scope="module")
    def load_config(self):
        get_test_config()

    @fixture(scope="function", params=get_test_config()["browser"])
    def course_page(self, request):
        config = get_test_config()
        browser = request.param
        print(browser)
        if browser == "chrome":
            options = webdriver.ChromeOptions()

            if config["headless"] == True:
                options.add_argument("--headless=new")

            driver = webdriver.Chrome(options=options)

        elif browser == "firefox":
            options = FirefoxOptions()

            if config["headless"] == True:
                options.add_argument("-headless")

            driver = webdriver.Firefox(options=options)
        else:
            raise ValueError(f"Browser {browser} is not supported")

        browser_size: str = config["browser_size"]
        if browser_size == "maximized":
            driver.maximize_window()
        else:
            browser_window_spec = browser_size.split("x")
            browser_window_width = int(browser_window_spec[0])
            browser_window_height = int(browser_window_spec[1])
            driver.set_window_size(browser_window_width, browser_window_height)

        driver.implicitly_wait(config["implicitly_wait"])
        driver.get(config["base_url"])
        home_page = HomePage(driver)

        signin_page = home_page.go_to_signin()

        dashboard_page = signin_page.login_valid_user(
            config["auth"]["teacher"]["username"],
            config["auth"]["teacher"]["password"],
        )

        my_course_page = dashboard_page.go_to_my_course()
        course_page = my_course_page.go_to_course(9)

        yield course_page

        driver.delete_all_cookies()
        driver.quit()

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_discussion", flow_name="simple_normal_flow"
        ),
    )
    def test_add_discussion_simple_normal_flow(
        self, course_page: project_3.pages.CoursePage.CoursePage, testcase: dict
    ):
        forum_page = course_page.go_to_forum(forum_id=327)
        forum_page.post_discussion(testcase["subject"], testcase["content"])
        discussion_page = forum_page.go_to_latest_discussion()

        assert discussion_page.get_discussion_subject() == testcase["subject"]
        assert discussion_page.get_discussion_content() == testcase["content"]

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_discussion", flow_name="simple_error_flow"
        ),
    )
    def test_add_discussion_simple_error_flow(
        self, course_page: project_3.pages.CoursePage.CoursePage, testcase: dict
    ):
        forum_page = course_page.go_to_forum(forum_id=327)
        forum_page.post_discussion(testcase["subject"], testcase["content"])

        if "subject_error" in testcase:
            assert forum_page.get_subject_error() == testcase["subject_error"]

        if "content_error" in testcase:
            assert forum_page.get_content_error() == testcase["content_error"]

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_discussion", flow_name="simple_normal_flow"
        ),
    )
    def test_add_discussion_advance_normal_flow(
        self, course_page: project_3.pages.CoursePage.CoursePage, testcase
    ):
        forum_page = course_page.go_to_forum(forum_id=327)
        advance_add_discussion_page = forum_page.go_to_advance_add_page()
        forum_page = advance_add_discussion_page.post_valid_discussion(
            testcase["subject"], testcase["content"]
        )
        discussion_page = forum_page.go_to_latest_discussion()

        assert discussion_page.get_discussion_subject() == testcase["subject"]
        assert discussion_page.get_discussion_content() == testcase["content"]

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_discussion", flow_name="simple_error_flow"
        ),
    )
    def test_add_discussion_advance_error_flow(
        self, course_page: project_3.pages.CoursePage.CoursePage, testcase: dict
    ):
        forum_page = course_page.go_to_forum(forum_id=327)
        advance_add_discussion_page = forum_page.go_to_advance_add_page()
        advance_add_discussion_page = (
            advance_add_discussion_page.post_invalid_discussion(
                testcase["subject"], testcase["content"]
            )
        )

        if "subject_error" in testcase:
            assert (
                advance_add_discussion_page.get_subject_error()
                == testcase["subject_error"]
            )

        if "content_error" in testcase:
            assert (
                advance_add_discussion_page.get_content_error()
                == testcase["content_error"]
            )

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_discussion", flow_name="upload_file_normal"
        ),
    )
    def test_add_discussion_advance_file_normal_flow(
        self,
        tmp_path,
        course_page: project_3.pages.CoursePage.CoursePage,
        testcase: dict,
    ):
        file_size: float = testcase["file_size"]
        forum_page = course_page.go_to_forum(forum_id=327)
        advance_add_discussion_page = forum_page.go_to_advance_add_page()
        advance_add_discussion_page.post_valid_discussion(
            "Test", "Test", str(gen_file_in_path(tmp_path, file_size))
        )

        discussion_page = forum_page.go_to_latest_discussion()

        assert discussion_page.get_discussion_subject() == "Test"
        assert discussion_page.get_discussion_content() == "Test"

        expected_file_name = str(file_size).replace(".", "_") + "KB.txt"

        assert (
            discussion_page.get_discussion_attachment_file_list()[0]
            == expected_file_name
        )

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_discussion", flow_name="upload_file_too_large"
        ),
    )
    def test_add_discussion_advance_file_large_flow(
        self,
        tmp_path,
        course_page: project_3.pages.CoursePage.CoursePage,
        testcase: dict,
    ):
        file_size: float = testcase["file_size"]
        forum_page = course_page.go_to_forum(forum_id=327)
        advance_add_discussion_page = forum_page.go_to_advance_add_page()
        advance_add_discussion_page.post_large_file_to_discussion(
            "Test", "Test", str(gen_file_in_path(tmp_path, file_size))
        )
        assert advance_add_discussion_page.get_file_upload_error() == "maxbytesfile"

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_discussion", flow_name="upload_file_too_large_php"
        ),
    )
    @pytest.mark.xfail()
    def test_add_discussion_advance_file_large_flow(
        self,
        tmp_path,
        course_page: project_3.pages.CoursePage.CoursePage,
        testcase: dict,
    ):
        file_size: float = testcase["file_size"]
        forum_page = course_page.go_to_forum(forum_id=327)
        advance_add_discussion_page = forum_page.go_to_advance_add_page()
        advance_add_discussion_page.post_large_file_to_discussion(
            "Test", "Test", str(gen_file_in_path(tmp_path, file_size))
        )
        assert advance_add_discussion_page.get_file_upload_error() == "maxbytesfile"
