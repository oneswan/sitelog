import requests
import time
import re
import logging


class SiteStatusChecker(object):

    def __init__(self, timeout=10):
        self.logger = logging.getLogger(__name__)
        self.timeout = timeout

    def _check_site_status(self, url):
        '''
        Returns:
            (status): Boolean - Whether reached the website or not?
            (timetaken): Float - Time it took for fetching a response
            (response_status_code): Int - Status Code Returned by the Website.
        '''
        start_timer = time.time()
        try:
            siteResponse = requests.get(url, timeout=self.timeout)
            end_timer = time.time()
            if siteResponse.status_code in (200, 302):
                return True, round(end_timer - start_timer, 4), siteResponse.status_code
            else:
                return False, round(end_timer - start_timer, 4), siteResponse.status_code
        except Exception as e:
            print("Exception Occured:", e)
            return False, None, None

    def _get_normalized_url(self, url):
        '''
        Add http:// in front of the url if it doesn't have.
        '''
        if not re.match('^http[s]?://', url):
            url = 'http://' + url
        return url

    def check_internet_status(self):
        '''
        Checks if Google or Facebook can be reached.

        If True, Conclude that Internet is available.
        '''
        googleUp, googleTime, googleStatus = self._check_site_status('http://www.google.com')
        fbUp, fbTime, fbStatus = self._check_site_status('http://www.facebook.com')

        if googleUp or fbUp:
            return True
        return False

    def check_status_repeatedly(self, urls, times=5000, interval_between=5):
        try:
            urls = map(self._get_normalized_url, urls)

            for _ in range(times):
                if not self.check_internet_status():
                    self.logger.debug("No Internet Available. Waiting...")
                    continue

                self.logger.debug("Internet is Available. Checking the urls...")
                for url in urls:
                    url_up, url_time, url_status_code = self._check_site_status(url)
                    if url_up:
                        print("%s is up. It took %.3f seconds to load. Code: %s" % (url, url_time, url_status_code))
                    elif url_status_code is not None:
                        print("%s looks like its down. Time Taken: %.3f. Code: %s" % (url, url_time, url_status_code))
                    else:
                        print("%s is down." % (url))

                time.sleep(interval_between * 60)
            return True

        except Exception as e:
            print("Exception Occured:", e)
            return False
