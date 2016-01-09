from .Site import Site
from .Paste import Paste
from bs4 import BeautifulSoup
from . import helper
from time import sleep
from settings import SLEEP_PASTEBIN
from twitter import TwitterError
import requests
import logging


class PastebinPaste(Paste):
    def __init__(self, id):
        self.id = id
        self.headers = None
        self.url = 'http://pastebin.com/raw/{0}'.format(self.id)
        self.tweet_url = 'http://pwnmon.com/1/raw/{0}'.format(self.id)
        self.log = logging.getLogger('pastebin')
        super(PastebinPaste, self).__init__()


class Pastebin(Site):
    def __init__(self, last_id=None):
        if not last_id:
            last_id = None
        self.ref_id = last_id
        self.BASE_URL = 'http://pastebin.com'
        self.sleep = SLEEP_PASTEBIN
        self.session = requests.Session()
        self.log = logging.getLogger('pastebin')
        super(Pastebin, self).__init__()

    def update(self):
        '''update(self) - Fill Queue with new Pastebin IDs'''
        new_pastes = []
        #if not self.ref_id:
        self.log.info('Retrieving ID\'s')
        results = BeautifulSoup(self.session.get(self.BASE_URL).text).find_all(lambda tag: tag.name == 'li' and tag.a)        
        #results += BeautifulSoup(self.session.get(self.BASE_URL + '/archive').text).find_all(lambda tag: tag.name == 'td' and tag.a and '/archive/' not in tag.a['href'] and tag.a['href'][1:])
        if not self.ref_id:
            results = results[:60]
        for entry in results:
            paste = PastebinPaste(entry.a['href'][1:])
            # Check to see if we found our last checked URL
            if paste.id == self.ref_id:
                break
            new_pastes.append(paste)
        for entry in new_pastes[::-1]:
            self.log.warning('Adding URL: {0}'.format(entry.url))
            self.put(entry)
    def get_paste_text(self, paste):
        return helper.download(paste.url)
