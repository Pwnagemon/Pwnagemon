# settings.py

USE_DB = True
DB_HOST = 'localhost'
DB_PORT = 27017
SMTP_SERVER = '[mail server host name]'
SMTP_PORT = [relay_port]
SMTP_USER = '[email address]'
SMTP_PASS = '[pass]'

# Twitter Settings
CONSUMER_KEY = '[hash]'
CONSUMER_SECRET = '[hash]'
ACCESS_TOKEN = '[hash]'
ACCESS_TOKEN_SECRET = '[hash]'

# Thresholds
EMAIL_THRESHOLD = 20
HASH_THRESHOLD = 30
DB_KEYWORDS_THRESHOLD = .55

# Time to Sleep for each site
SLEEP_SLEXY = 60
SLEEP_PASTEBIN = 15
SLEEP_PASTIE = 30

# Other configuration
tweet_history = "tweet.history"
