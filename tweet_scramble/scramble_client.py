import tweepy
from lyricscramble import LyricScrambler
import re
import string


class LyricScrambleTwitterClient():
    """Tweets scrambled phrases built from song lyrics."""

    def __init__(self, OAuth):
        """Initializes the ScrambleClient."""

        # Get API reference
        self._api = tweepy.API(OAuth)

        # Get lyricscrambler instance
        self._scrambler = LyricScrambler(max_songs=3)

        # Instantiate logging
        # self._log = logging.get_logger()

    def _extract_request(self, raw):
        """Given a raw request string, returns the artist and song."""

        #TODO: the text of the tweet contains encoded punctuation. i.e & is amp

        # Convert the text to UTF-8
        s = raw.encode('utf-8', 'replace')

        # Parse out any handles or hashtags
        clean = re.sub('(@\S+)|(#\S+)', '', s)

        # Split on '->' and strip leading/trailing white space
        request = clean.split('-&gt;')

        # Remove any remaining punctuation
        table = string.maketrans("", "")
        request = [field.translate(table, string.punctuation) for field in request]

        # Ensure size of request is 2
        if len(request) is not 2:
            raise ValueError("The song request was malformed.")

        # Return request
        return request

    def handle_request(self, raw_request, sender):
        """Adds the requested song's lyrics to the corpus and (might)
           tweet a scrambled response based on the corpus. Returns True
           if the song is successfully added to the corpus; False otherwise."""

        # Get the request from the raw tweet request
        try:
            artist, title = self._extract_request(raw_request)
        except ValueError, e:
            print e
            return False

        # Attempt to add the song to the scrambler corpus
        if not self._scrambler.add_song(artist, title):
            print 'Could not find the requested song lyrics for %s %s' % (artist, title)
            return False

        # If appropriate, tweet a response!
        if self._time_to_tweet():
            print "Tweeting a song."
            self._tweet_response(sender)

        return True

    def _time_to_tweet(self):
        """Returns true if the conditions to tweet are met."""

        # For now, just always respond
        return True

    def _tweet_response(self, recipient):
        """Tweets a scrambled phrase based on the current song corpus."""

        # Generate phrase that's no more than 140 chars and at least 5 words
        size_limit = 140 - (len(recipient) + 2)
        phrase = self._scrambler.get_phrase(max_size=size_limit, min_words=5)

        # Construct message
        msg = '@%s %s' % (recipient, phrase)

        # Tweet
        print 'Tweeting: ' + msg
        self._api.update_status(msg)
