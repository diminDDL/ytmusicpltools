# ytmusicpltools
[![Made in Ukraine](https://img.shields.io/badge/made_in-ukraine-ffd700.svg?labelColor=0057b7)](https://vshymanskyy.github.io/StandWithUkraine)
</br>
A few python scripts to download liked music from ytmusic or add all liked songs to another playlist. Now with spotify import support!
Each folder has all the files needed to run self-contained.
The only setup required is to set your own cookies in the [headers_auth_example.json](../main/headers_auth_example.json) file, rename it to just `headers_auth.json` and install [ytmusicapi](https://github.com/sigma67/ytmusicapi).
If you need spotify features you need to install [spotipy](https://github.com/spotipy-dev/spotipy) and set the API data in a spotify_secrets.json, same way as with the youtube stuff, but this time they can be generated [here](https://developer.spotify.com/dashboard).
More info can be found in the official [ytmusicapi](https://github.com/sigma67/ytmusicapi) page.
