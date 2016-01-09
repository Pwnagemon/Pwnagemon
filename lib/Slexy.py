from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_SLEXY
from twitter import TwitterError
import logging


class SlexyPaste(Paste):
    def __init__(self, id):
        self.id = id
        self.headers = {'Referer': 'http://slexy.org/view/{0}'.format(self.id)}
        self.url = 'http://slexy.org/raw/{0}'.format(self.id)
        self.tweet_url = 'http://pwnmon.com/3/raw/{0}'.format(self.id)
        self.log = logging.getLogger('slexy')
        super(SlexyPaste, self).__init__()


class Slexy(Site):
    def __init__(self, last_id=None):
        if not last_id:
            last_id = None
        self.ref_id = last_id
        self.BASE_URL = 'http://slexy.org'
        self.sleep = SLEEP_SLEXY
        self.log = logging.getLogger('slexy')
        super(Slexy, self).__init__()

    def update(self):
        '''update(self) - Fill Queue with new Slexy IDs'''
        self.log.info('[*] Retrieving ID\'s')
        results = BeautifulSoup(helper.download(self.BASE_URL + '/recent')).find_all(lambda tag: tag.name == 'td' and tag.a and '/view/' in tag.a['href'])
        new_pastes = []
        if not self.ref_id:
            results = results[:60]
        for entry in results:
            paste = SlexyPaste(entry.a['href'].replace('/view/', ''))
            # Check to see if we found our last checked URL
            if paste.id == self.ref_id:
                break
            new_pastes.append(paste)
        for entry in new_pastes[::-1]:
            self.log.warning('[+] Adding URL: {0}'.format(entry.url))
            self.put(entry)

    def get_paste_text(self, paste):
        return helper.download(paste.url, paste.headers)
