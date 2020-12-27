import tweepy

from .. import config

auth = tweepy.OAuthHandler(
    config.twitter_auth.CONSUMER_KEY, config.twitter_auth.CONSUMER_KEY_SECRET
)
auth.set_access_token(
    config.twitter_auth.ACCESS_TOKEN, config.twitter_auth.ACCESS_TOKEN_SECRET
)

api = tweepy.API(auth)
