import time
from selenium import webdriver

from selenium.webdriver.firefox.options import Options as FirefoxOptions

import pytest
from pytest import fixture
import project_3.pages.CoursePage

from project_3.pages.HomePage import HomePage
import project_3.pages.CoursePage
from project_3.utils.config import get_test_config, get_tests
from project_3.utils.gen_file import gen_file_in_path


class TestAddFileResource:
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
            feature_name="add_file_resource", flow_name="upload_file_normal"
        ),
    )
    def test_normal(
        self,
        tmp_path,
        course_page: project_3.pages.CoursePage.CoursePage,
        testcase: dict,
    ):
        name, size = testcase["name"], testcase["file_size"]

        course_page.toggle_edit_mode()
        add_file_page = course_page.go_to_add_file_page()
        add_file_page.fill_in_name(name)
        add_file_page.fill_in_description("This is a test file submitted")
        add_file_page.add_file_to_attachement_list(
            str(gen_file_in_path(tmp_path, size))
        )
        course_page = add_file_page.submit_resource()
        course_page.toggle_edit_mode()
        resource_name_and_links = course_page.get_list_of_file_resource()
        print(resource_name_and_links)
        resource_names, resource_links = zip(*resource_name_and_links)
        assert name in resource_names

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_file_resource", flow_name="file_not_selected"
        ),
    )
    def test_file_not_selected(
        self,
        course_page: project_3.pages.CoursePage.CoursePage,
        testcase: dict,
    ):
        name = testcase["name"]

        course_page.toggle_edit_mode()
        add_file_page = course_page.go_to_add_file_page()
        add_file_page.fill_in_name(name)
        add_file_page.fill_in_description("This is a test file submitted")
        course_page = add_file_page.submit_invalid_resource()

        assert "Required" == add_file_page.get_file_error()

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_file_resource", flow_name="file_name_too_long"
        ),
    )
    def test_file_name_too_long(
        self,
        course_page: project_3.pages.CoursePage.CoursePage,
        testcase: dict,
    ):
        name = testcase["name"]

        course_page.toggle_edit_mode()
        add_file_page = course_page.go_to_add_file_page()
        add_file_page.fill_in_name(name)
        add_file_page.fill_in_description("This is a test file submitted")

        assert "- Maximum of 255 characters" == add_file_page.get_name_error()

    @pytest.mark.parametrize(
        argnames="testcase",
        argvalues=get_tests(
            feature_name="add_file_resource", flow_name="file_too_large_php"
        ),
    )
    def test_file_too_large_php(
        self,
        tmp_path,
        course_page: project_3.pages.CoursePage.CoursePage,
        testcase: dict,
    ):
        name = testcase["name"]
        size = testcase["file_size"]

        course_page.toggle_edit_mode()
        add_file_page = course_page.go_to_add_file_page()
        add_file_page.fill_in_name(name)
        add_file_page.fill_in_description("This is a test file submitted")
        add_file_page.add_file_to_attachement_list(
            str(gen_file_in_path(tmp_path, size))
        )

        time.sleep(5)
