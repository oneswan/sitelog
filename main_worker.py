from status_checker import SiteStatusChecker
import logging
from utils import setup_logging


def main():
    setup_logging(default_path='logging_config.yaml')
    logger = logging.getLogger('main_worker')
    status_checker = SiteStatusChecker()
    logger.debug("Internet is available? => %s" % (status_checker.check_internet_status()))
    status_checker.check_status_repeatedly(interval_between=1)

if __name__ == '__main__':
    main()
