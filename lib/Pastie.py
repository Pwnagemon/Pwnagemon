from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_PASTIE
from twitter import TwitterError
import logging


class PastiePaste(Paste):
    def __init__(self, id):
        self.id = id
        self.headers = None
        self.url = 'http://pastie.org/pastes/{0}/text'.format(self.id)
        self.tweet_url = 'http://pwnmon.com/2/pastes/{0}/text'.format(self.id)
        self.log = logging.getLogger('pastie')
        super(PastiePaste, self).__init__()


class Pastie(Site):
    def __init__(self, last_id=None):
        if not last_id:
            last_id = None
        self.ref_id = last_id
        self.BASE_URL = 'http://pastie.org'
        self.sleep = SLEEP_PASTIE
        self.log = logging.getLogger('pastie')
        super(Pastie, self).__init__()

    def update(self):
        '''update(self) - Fill Queue with new Pastie IDs'''
        self.log.info('[*] Retrieving ID\'s')
        results = [tag for tag in BeautifulSoup(helper.download(self.BASE_URL + '/pastes')).find_all('p', 'link') if tag.a]
        new_pastes = []
        if not self.ref_id:
            results = results[:60]
        for entry in results:
            paste = PastiePaste(entry.a['href'].replace(self.BASE_URL + '/pastes/', ''))
            # Check to see if we found our last checked URL
            if paste.id == self.ref_id:
                break
            new_pastes.append(paste)
        for entry in new_pastes[::-1]:
            self.log.warning('Adding URL: {0}'.format(entry.url))
            self.put(entry)

    def get_paste_text(self, paste):
        return BeautifulSoup(helper.download(paste.url)).pre.text
