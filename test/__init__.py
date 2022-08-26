import logging
import logging.config
import os

import yaml
from dotenv import find_dotenv, load_dotenv


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


load_app_dotenv()
init_app_logging()

logger = logging.getLogger("fileLogger")
dockerLogger = logging.getLogger("dockerLogger")
