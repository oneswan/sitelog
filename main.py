import json
from status_checker import SiteStatusChecker
import logging.config
import os
import yaml


def setup_logging(default_path='logging.yaml', default_level=logging.INFO, env_key='LOG_CFG'):
    """
    Setup logging configuration
    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def main():
    setup_logging(default_path='logging_config.yaml')
    logger = logging.getLogger('main')
    status_checker = SiteStatusChecker()
    logger.debug("Internet is available? => %s" % (status_checker.check_internet_status()))
    status_checker.check_status_repeatedly(['trello.com', 'asana.com', 'falloutx.me'], times=1)

if __name__ == '__main__':
    main()
