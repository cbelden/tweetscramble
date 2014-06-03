import tweepy
from tweet_scramble import SongRequestListener, LyricScrambleTwitterClient
import os


# Get credentials
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Get authorization from Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Get the Twitter client
tweeter = LyricScrambleTwitterClient(auth)

# Get stream listener
listener = SongRequestListener(tweeter)

# Create stream and run
stream = tweepy.Stream(auth, listener)
stream.filter(track=['@lyricscramble'])
