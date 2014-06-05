import tweepy
from tweet_scramble import SongRequestHandler
import os


# Get credentials
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Get authorization from Twitter
oauth = tweepy.OAuthHandler(consumer_key, consumer_secret)
oauth.set_access_token(access_token, access_token_secret)

# Get twitter API
twitter = tweepy.API(oauth)

# Get stream listener
listener = SongRequestHandler(twitter)

# Listen to the stream of tweets/events specific to the bot's twitter account
stream = tweepy.Stream(oauth, listener)
stream.userstream(_with='user')
