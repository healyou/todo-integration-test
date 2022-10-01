import logging
import logging.config
import os
from pathlib import Path

import yaml
from selenium import webdriver
from dotenv import find_dotenv, load_dotenv

from test.utils.common_utils import get_project_root_str


def load_app_dotenv():
    dotenv_path = find_dotenv('.env')
    load_dotenv(dotenv_path)


def init_app_logging():
    with open(os.path.dirname(__file__) + '/../logging.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    log_output_path = os.path.dirname(__file__) + '/..' + os.environ["log_dir"]
    log_param_path_value = config["handlers"]["file"]["filename"].format(log_path=log_output_path)
    docker_log_param_path_value = config["handlers"]["dockerFile"]["filename"].format(log_path=log_output_path)
    config["handlers"]["file"]["filename"] = log_param_path_value
    config["handlers"]["dockerFile"]["filename"] = docker_log_param_path_value
    logging.config.dictConfig(config)


def check_load_chrome_driver(logger):
    logger.debug("check success load webdriver")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument('--window-size=1280,720')
    web_driver_path = str(Path(__file__).parent.parent) + os.environ['web_driver_path'] + '/' + os.environ['web_driver_name']

    driver = webdriver.Chrome(executable_path=web_driver_path, chrome_options=chrome_options)
    driver.get("chrome://settings/")
    driver.quit()

    logger.debug("webdriver load success")


load_app_dotenv()
init_app_logging()

logger = logging.getLogger("fileLogger")
dockerLogger = logging.getLogger("dockerLogger")

# Проверим, что тесты хотя бы запустятся, а потом работаем docker
check_load_chrome_driver(logger)
