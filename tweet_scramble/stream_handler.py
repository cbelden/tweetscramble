from tweepy import StreamListener


class SongRequestListener(StreamListener):
    """Handles data received from the stream."""

    def __init__(self, scramble_client):
        """Initializes twitter client for emitting scrambled phrases."""

        # The scramble client provides functionality to send status requests
        self._scramble_client = scramble_client

        # Call StreamListener constructor
        super(SongRequestListener, self).__init__()

    def on_status(self, status):

        # Add song request the scrambler's corpus
        request = status.text
        sender_handle = status.user.screen_name

        if self._scramble_client.handle_request(request, sender_handle):
            print 'Handled a song request'
        else:
            print 'Could not handle the request.'

        return True

    def on_error(self, status_code):
        print 'Got an error with status code: ' + str(status_code)
        return True

    def on_timeout(self):
        print 'Timeout...'
        return True
