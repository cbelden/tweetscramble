#tweetscramble

##About
tweetscramble is a Twitter bot that leverages the functionality in a few of my other projects to listen to
song requests via Twitter and tweet scrambled phrases based on the lyrics in the
requested songs.

NOTE: this thing is in total alpha mode; errors are to be expected.

###Use
On Twitter, tweet a song request using the following syntax:

"@lyricscramble artist -> song_title"

The lyricscramble bot will then tweet a scrambled phrase at you composed of words from
the last three song requests. In the event of a failure, the bot should tweet an
explanation.

###How it works
Using tweepy, I listen to the stream of tweets directed to the Twitter
handle, @lyricscramble. Upon a received tweet, the song information is extracted from the tweet
(if the tweet is formatted for a song request).

At this time, the lyrics for the song are queried, and if they are found, the lyrics
are added to a corpus. Using this corpus, a Markov chain is created, and a phrase
is generated that is then tweeted in response to the original request. The corpus
may be periodically refreshed, and it will normally include the last three song requests.

