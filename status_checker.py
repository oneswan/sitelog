import requests
import time
import re
import logging

from models import Site, Response, db_session


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

    def check_status_repeatedly(self, times=5000, interval_between=5):
        try:
            sites = db_session.query(Site).all()

            for _ in range(times):
                if not self.check_internet_status():
                    self.logger.debug("No Internet Available. Waiting...")
                    continue

                self.logger.debug("Internet is Available. Checking the urls...")
                for site in sites:
                    url = self._get_normalized_url(site.url)
                    print("checking %s" % url)
                    url_up, url_time, url_status_code = self._check_site_status(url)
                    if url_up:
                        self.logger.debug("%s is up. It took %.3f seconds to load. Code: %s" % (url, url_time, url_status_code))
                    elif url_status_code is not None:
                        self.logger.debug("%s looks like its down. Time Taken: %.3f. Code: %s" % (url, url_time, url_status_code))
                    else:
                        self.logger.debug("%s is down." % (url))

                    self.logger.debug("Adding the Response to DB")
                    try:
                        resp = Response(site, url_up, code=url_status_code, time_taken=url_time)
                        db_session.add(resp)
                        db_session.commit()
                    except Exception as e:
                        self.logger.debug("Database Exception Occcured while adding response to the DB: %s", e)

                time.sleep(interval_between * 60)
            return True

        except Exception as e:
            print("Exception Occured:", e)
            return False
