import tweepy
import re
from lyricscramble import LyricScrambler


class SongRequestHandler(tweepy.StreamListener):
    """Handles song requests received from a Twitter stream."""

    def __init__(self, twitterAPI):
        """Initializes twitter client for emitting scrambled phrases."""

        self._scrambler = LyricScrambler()      # produces scrambled phrases
        self._twitter = twitterAPI              # access to Twitter functionality

        # Name of associated twitter account
        self._screen_name = self._twitter.me().screen_name

        # Call StreamListener constructor
        super(SongRequestHandler, self).__init__()

    def on_error(self, status_code):
        print 'Got an error with status code: ' + str(status_code)
        return True

    def on_timeout(self):
        print 'Timeout...'
        return True

    def on_status(self, status):

        # Don't process tweets that we've created
        if status.user.screen_name == self._screen_name:
            return True

        request = status.text
        sender_handle = status.user.screen_name
        tweetID = status.id

        print "Recieved a song request: %s" % (request)

        # Handle incoming song request
        self._handle_request(request, sender_handle, tweetID)

        return True

    def _handle_request(self, raw_request, sender, tweetID):
        """Adds the requested song's lyrics to the corpus and (might) tweet a scrambled response based on the corpus."""

        # Store any errors
        error_msg = ''

        # Get the request from the raw tweet text
        try:
            artist, title = self._extract_request(raw_request)
        except ValueError, e:
            print '\t%s' % (str(e))
            error_msg = "Sorry @%s, your song request was not formatted correctly." % (sender)

        # Attempt to add the song to the scrambler corpus
        if not error_msg and not self._scrambler.add_song(artist, title):
            error_msg = "Sorry @%s, couldn't find the song: %s- %s" % (sender, artist, title)

        # Handle any errors that occured; tell sender the request failed
        if error_msg:

            try:
                self._twitter.update_status(error_msg, tweetID)
            except tweepy.TweepError, e:
                print "\tCouldn't tweet error response."
                print "\t\t%s" % (str(e))

            print "\tCould not handle the request."
            return

        # If appropriate, tweet a response!
        print "\tHandled the song request."
        if self._time_to_tweet():
            self._tweet_response(sender, tweetID)

    def _extract_request(self, raw):
        """Given a raw request string, returns the artist and song."""

        #TODO: the text of the tweet contains encoded punctuation. i.e & is amp

        # Convert the text to UTF-8
        s = raw.encode('utf-8', 'replace')

        # Parse out any handles or hashtags
        clean = re.sub('(@\S+)|(#\S+)', '', s)

        # Split on '->' and strip leading/trailing white space
        request = clean.split('-&gt;')

        # Ensure size of request is 2
        if len(request) is not 2:
            raise ValueError("The song request was malformed.")

        # Return request
        return request

    def _time_to_tweet(self):
        """Returns true if the conditions to tweet are met."""

        # For now, just always respond
        return True

    def _tweet_response(self, recipient, tweetID):
        """Tweets a scrambled phrase based on the current song corpus."""

        # Generate phrase that's no more than 140 chars and at least 5 words
        handle = '@%s ' % (recipient)
        phrase_size_limit = 140 - len(handle)
        phrase = self._scrambler.get_phrase(max_size=phrase_size_limit, min_words=5)

        # Construct message
        msg = '%s%s' % (handle, phrase)

        # Tweet
        print '\tTweeting: ' + msg
        self._twitter.update_status(msg, tweetID)
