#! /usr/bin/env python
# pwnagemon.py

from lib.helper import createThread
from lib.regexes import regexes
from lib.Pastebin import Pastebin, PastebinPaste
from lib.Slexy import Slexy, SlexyPaste
from lib.Pastie import Pastie, PastiePaste
#from lib.Ghostbin import Ghostbin, GhostbinPaste
#from lig.Reddit import Reddit, RedditPaste
#from lib.Twitter import Twitter, TwitterPaste
from time import sleep
from twitter import Twitter, OAuth
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import threading
import logging
import logging.config
import coloredlogs

def monitor():
    logging.config.fileConfig('logger.conf')

    logging.warning('Monitoring...')
    
    bot = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET))
    
    # Create lock for tweet action
    tweet_lock = threading.Lock()

    pastebin_thread = createThread(Pastebin().monitor, bot, tweet_lock)
    slexy_thread = createThread(Slexy().monitor, bot, tweet_lock)
    pastie_thead = createThread(Pastie().monitor, bot, tweet_lock)

    # Let threads run
    try:
        while(1):
            sleep(5)
    except KeyboardInterrupt:
        logging.warning('Stopped.')

if __name__ == "__main__":
    monitor()
