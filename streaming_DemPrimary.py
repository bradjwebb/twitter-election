# This script streams tweets using the twitter API to a log file.
# The keywords for the search are dictated by the keywords.py script
# dir: %homepath%\Desktop\Winter\DtMin\"Data Mining Project"\"Python Scripts"\


import logging
from keywords import keyword_search
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from logging.handlers import TimedRotatingFileHandler

access_token = 'xxxxxxxxxxxx'
# Access Token
access_token_secret = 'xxxxxxxxxxxx'
# Secret Access Token
consumer_key = 'xxxxxxxxxxxx'
# API Key
consumer_secret = 'xxxxxxxxxxxx'
# API secret


loghandler = TimedRotatingFileHandler(
    'election_stream',
    when='midnight',
)

logger = logging.getLogger('Election Logger')  # instantiates new log
logger.addHandler(loghandler)
logger.setLevel(logging.INFO)


class StdOutListener(StreamListener):
    # Basic listener that prints received tweets to stdout
    def on_data(self, data):
        logger.info(data)

    def on_error(self, status):
        logger.info(status)

if __name__ == '__main__':

    # Handles twitter authentication and the connection to Twitter
    # Streaming API

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This is the stream filter: see keywords.py to get search values
    stream.filter(track=keyword_search)
