import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from time import sleep

deduplicate = False  # Set to True to remove duplicate tracks from the playlist
debug = False  # Set to True to enable debug output
chunk_size = 50  # Number of tracks to add per API call
load_limit = 5000  # Number of tracks to load from Spotify per API call
sleep_time = 2  # Seconds to wait between API calls

# Load Spotify credentials from an external file
with open('../spotify_secrets.json') as f:
    spotify_secrets = json.load(f)

# Set up authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_secrets['client_id'],
                                               client_secret=spotify_secrets['client_secret'],
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='user-library-read playlist-read-private'))

ytmusic = YTMusic('../headers_auth.json')  # assuming you have already authenticated and saved your headers to a file

# Test if we authenticated correctly
try:
    liked_songs = ytmusic.get_liked_songs(limit=1)
    print("Successfully authenticated to YouTube Music API!")
except Exception as e:
    print(e)
    print("Failed to authenticate to YouTube Music API. Please edit headers_auth.json and try again.")
    exit()


def chunkify(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def contains_track_id(track_id, track_dict):
    for i in track_dict:
        if i['videoId'] == track_id:
            return True
    return False


def convert_liked_songs():
    # Initialize variables
    offset = 0
    ytmusic_track_ids = []

    while True:
        # Get liked songs from Spotify with pagination
        spotify_tracks = sp.current_user_saved_tracks(limit=50, offset=offset)
        total_tracks = spotify_tracks['total']

        if not spotify_tracks['items']:
            break  # Exit the loop when no more tracks are returned

        print(f"Converting {total_tracks} liked songs from offset {offset}...")

        for index, item in enumerate(spotify_tracks['items'], start=offset + 1):
            track = item['track']
            search_query = f"{track['artists'][0]['name']} - {track['name']}"
            print(f"Processing track {index} of {total_tracks}: {search_query}")
            search_result = ytmusic.search(search_query, filter='songs')
            if search_result:
                ytmusic_track_ids.append(search_result[0]['videoId'])
            else:
                print(f"Track not found on YouTube Music: {search_query}")
        
        offset += len(spotify_tracks['items'])  # Update the offset for the next iteration
    
    print(f"Found {len(ytmusic_track_ids)} of {total_tracks} tracks on YouTube Music")

    # Like the songs on YouTube Music in chunks
    print("Liking songs on YouTube Music...")
    total = 0
    liked_songs_ytm = ytmusic.get_liked_songs(limit=load_limit)['tracks']

    # reverse the list so that the oldest songs are liked first
    ytmusic_track_ids.reverse()
    
    for i, chunk in enumerate(chunkify(ytmusic_track_ids, chunk_size), start=1):
        if deduplicate:
            for track in chunk:
                if contains_track_id(track, liked_songs_ytm):
                    chunk.remove(track)
                    print(f"Track {track} already liked, skipping...")

        print(f"Processing chunk {i}...")
        for track_id in chunk:
            resp = ytmusic.rate_song(track_id, 'LIKE')
            total += 1

            if debug:
                print(resp)

            sleep(sleep_time)  # Prevent YouTube Music rate limiting
    
    print(f"Liked {total} songs on YouTube Music")

    print("Conversion complete!")


# Convert liked Spotify songs to liked songs on YouTube Music
convert_liked_songs()