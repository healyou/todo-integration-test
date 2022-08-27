import os

import pytest
from selenium import webdriver

from test import logger, dockerLogger
from test.actions.web_driver_actions import WebDriverActions
from test.docker.docker_compose import TodoAppDockerCompose, get_web_app_host
from test.utils.common_utils import get_project_root_str


@pytest.fixture(scope='session', autouse=True)
def todo_app_compose():
    logger.debug("setup docker")
    compose = setup_todo_app_docker_compose()

    yield compose

    logger.debug("teardown docker")
    teardown_todo_app_docker_compose(compose)


@pytest.fixture(scope='function')
def web_driver():
    logger.debug("setup webdriver")
    driver = setup_chrome_web_driver()

    yield driver

    logger.debug("teardown webdriver")
    driver.quit()


@pytest.fixture
def web_driver_actions(web_driver):
    return WebDriverActions(web_driver)


def setup_chrome_web_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--window-size=1280,720')
    web_driver_path = get_project_root_str() + os.environ['web_driver_path'] + '/' + os.environ['web_driver_name']
    return webdriver.Chrome(executable_path=web_driver_path, chrome_options=chrome_options)


def log_docker_callback(line: str):
    dockerLogger.debug(line)


def setup_todo_app_docker_compose() -> TodoAppDockerCompose:
    compose = TodoAppDockerCompose()
    compose.start()

    compose.follow_logs(log_docker_callback)

    host = get_web_app_host()
    port = compose.get_web_app_port()
    logger.debug("Docker host = " + host)
    logger.debug("Docker port = " + port)

    logger.debug("Wait for todo-app is started")
    compose.wait_for("http://{}:{}".format("127.0.0.1", port))
    logger.debug("todo-app is started")

    return compose


def teardown_todo_app_docker_compose(compose):
    compose.stop()
