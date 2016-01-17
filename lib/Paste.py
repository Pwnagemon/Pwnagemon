from .regexes import regexes
from settings import EMAIL_THRESHOLD, HASH_THRESHOLD, DB_KEYWORDS_THRESHOLD 
import re
from enum import IntEnum
import helper

class DumpType(IntEnum):
    NONE = 0
    DATABASE = 1
    CISCO = 2
    HONEYPOT = 4
    GOOGLE_API = 8
    PGP_PRIVATE = 16
    SSH_PRIVATE = 32
    CREDENTIALS = 64

class Paste(object):
    def __init__(self):
        '''
        class Paste: Generic "Paste" object to contain attributes of a standard paste

        '''
        self.emails = 0
        self.critical_emails = 0
        self.hashes = 0
        self.passwords = 0
        self.num_emails = 0
        self.num_critical_emails = 0
        self.num_hashes = 0
        self.num_passwords = 0
        self.text = None
        self.type = DumpType.NONE
        self.sites = None
        self.db_keywords = 0.0

    def match(self):
        '''
        Matches the paste against a series of regular expressions to determine if the paste is 'interesting'

        Sets the following attributes:
                self.emails
                self.hashes
                self.passwords
                self.num_emails
                self.num_hashes
                self.num_passwords
                self.db_keywords
                self.type

        '''
        # Get the amount of emails
        self.emails = list(set(regexes['email'].findall(self.text)))
        self.passwords = list(set(regexes['email_pass'].findall(self.text)))
        self.hashes = regexes['hash32'].findall(self.text)
        
        self.num_emails = len(self.emails)
        self.num_passwords = len(self.passwords)
        self.num_hashes = len(self.hashes)
        if self.num_emails > 0:
            self.sites = list(set([re.search('@(.*)$', email).group(1).lower() for email in self.emails]))
        
        display = ""
        i = 0
        for regex in regexes['critical_keywords']:
            display += '-'
            if regex.search(self.text):
                display = display[:-1] + '0'
                self.log.critical('sending email of {0} to {1}'.format(regexes['critical_alert_emails'][i], self.tweet_url))
                helper.alert_email(regexes['critical_alert_emails'][i], self.tweet_url)
                i += 1
        self.log.critical('[{0}] critical keywords'.format(display))
        display = ""
        for regex in regexes['db_keywords']:
            display += "-"
            if regex.search(self.text):
                display = display[:-1] + "0"
                self.db_keywords += round(1/float(len(regexes['db_keywords'])), 2)
        self.log.critical('[{0}] database keywords'.format(display))
        display = ''
        for regex in regexes['blacklist']:
            display += "-"
            if regex.search(self.text):
                display = display[:-1] + "0" 
                self.db_keywords -= round(1.25 * (1/float(len(regexes['db_keywords']))), 2)
        self.log.critical('[{0}] blacklist'.format(display))
        if (self.num_passwords > 0):
            self.type |= DumpType.CREDENTIALS
        if (self.num_emails >= EMAIL_THRESHOLD) or (self.num_hashes >= HASH_THRESHOLD) or (self.db_keywords >= DB_KEYWORDS_THRESHOLD):
            self.type |= DumpType.DATABASE
        if regexes['cisco_hash'].search(self.text) or regexes['cisco_pass'].search(self.text):
            self.type |= DumpType.CISCO
        if regexes['honeypot'].search(self.text):
            self.type |= DumpType.HONEYPOT
        if regexes['google_api'].search(self.text):
            self.type |= DumpType.GOOGLE_API
        if regexes['pgp_private'].search(self.text):
            self.type |= DumpType.PGP_PRIVATE
        if regexes['ssh_private'].search(self.text):
            self.type |= DumpType.SSH_PRIVATE
        # if regexes['juniper'].search(self.text): self.type = 'Juniper'
        for regex in regexes['banlist']:
            if regex.search(self.text):
                self.type = DumpType.NONE
                break
        return self.type
