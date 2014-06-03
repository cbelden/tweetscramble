#tweetscramble

##About
This project leverages the functionality in a few of my other projects to listen to
song requests via Twitter and tweet scrambled phrases based on the lyrics in the
requested songs.

##How it works
Using tweepy, I create and listen to the stream of tweets directed to the Twitter
handle, @lyricscramble. If the tweet is formatted for a song request, the artist
and title are extracted from the tweet.

At this time, the lyrics for the song are queried, and if they are found, the lyrics
are added to a corpus. Using this corpus, a Markov chain is created, and a phrase
is generated that is then tweeted in response to the original song request. The corpus
may be periodically refreshed, and it will normally include the last three song requests.

##Sample song request
"@lyricscramble Drake -> Marvins Room"

The song requests must be tweeted at the @lyricscramble handle, and the text must have the
form: artist -> title.
