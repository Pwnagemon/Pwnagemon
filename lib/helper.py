'''
helper.py - provides misc. helper functions

'''

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import requests
from time import sleep
import logging
import threading
from .Paste import DumpType
from settings import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS

r = requests.Session()
 
def createThread(target, *args):
    t = threading.Thread(target=target, args=args)         
    t.daemon = True
    t.start()
    return t
             
def alert_email(to, body):
    logging.critical('sending alert mail to {0}'.format(to))
    
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = to
    msg['Subject'] = "Pwnagemon Alert!"
    msg.attach(MIMEText(body, 'plain'))

    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.ehlo()
    mail.starttls()
    mail.login(SMTP_USER, SMTP_PASS)
    mail.sendmail(SMTP_USER, to, msg.as_string())
    mail.quit()

def download(url, headers=None):
    if not headers:
        headers = None
    if headers:
        r.headers.update(headers)
    try:
        response = r.get(url).text
    except requests.ConnectionError:
        logging.critical('[!] Critical Error - Cannot connect to site {0}'.format(url))
        sleep(5)
        logging.critical('[!] Retrying...{0}'.format(url))
        response = download(url)
    return response


def build_tweet(paste):
    '''
    build_tweet(url, paste) - Determines if the paste is interesting and, if so, builds and returns the tweet accordingly

    '''
    tweet = None
    if paste.match():
        paste.log.error('Paste matched.')
        tweet = paste.tweet_url      
        if paste.type & DumpType.CREDENTIALS:
            tweet += ' Credentials: {0}'.format(paste.num_passwords)
            paste.log.error(paste.passwords)
        if paste.type & DumpType.DATABASE:
            if paste.num_emails > 0:
                tweet += ' Emails: {0}'.format(paste.num_emails)
                paste.log.error(paste.emails)
            if paste.num_hashes > 0:
                tweet += ' Hashes: {0}'.format(paste.num_hashes)
                paste.log.error(paste.hashes)
            tweet += ' Keywords: {0}'.format(paste.db_keywords)
        if paste.type & DumpType.GOOGLE_API:
            tweet += ' Possible Google API key(s)'
        if paste.type & DumpType.CISCO:
            tweet += ' Possible CISCO configuration'
        if paste.type & DumpType.SSH_PRIVATE:
            tweet += ' Possible SSH private key'
        if paste.type & DumpType.HONEYPOT:
            tweet += ' Possible Honeypot Log'
        if paste.type & DumpType.PGP_PRIVATE:
            tweet += ' Possible PGP Private Key'
        tweet += ' #infoleak'
    return tweet
