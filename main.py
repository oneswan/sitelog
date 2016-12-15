import json
from status_checker import SiteStatusChecker


def main():
    status_checker = SiteStatusChecker()
    print("Internet is available? =>", status_checker.check_internet_status())
    status_checker.check_status_repeatedly(['trello.com', 'asana.com', 'falloutx.me'], times=1)

if __name__ == '__main__':
    main()
