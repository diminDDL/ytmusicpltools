import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
from time import sleep

deduplicate = False # Set to True to remove duplicate tracks from the playlist
debug = False # Set to True to enable debug output
chunk_size = 50 # Number of tracks to add per API call
load_limit = 5000 # Number of tracks to load from Spotify per API call
sleep_time = 2 # Seconds to wait between API calls
playlis = "2Oa5Tjb4DZGgAOuM5PgUsk"  # Spotify playlist ID


# Load Spotify credentials from an external file
with open('../spotify_secrets.json') as f:
    spotify_secrets = json.load(f)

# Set up authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_secrets['client_id'],
                                               client_secret=spotify_secrets['client_secret'],
                                               redirect_uri='http://localhost:8888/callback',
                                               scope='user-library-read playlist-read-private'))

ytmusic = YTMusic('../headers_auth.json')  # assuming you have already authenticated and saved your headers to a file

# test if we authenticated correctly
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

def ContainsTrackId (TrackId, TrackDict):
    for i in TrackDict:
        if i['videoId'] == TrackId:
            return True
    return False

def convert_playlist(spotify_playlist_id):
    # Get playlist details from Spotify
    spotify_playlist = sp.playlist(spotify_playlist_id)
    
    print(f"Converting playlist: {spotify_playlist['name']}")

    # Prepare track list for YouTube Music
    ytmusic_track_ids = []
    
    # Fetch tracks from Spotify with pagination
    offset = 0
    while True:
        spotify_tracks = sp.playlist_tracks(spotify_playlist_id, offset=offset)
        if not spotify_tracks['items']:
            break  # Exit the loop when no more tracks are returned
        
        for index, item in enumerate(spotify_tracks['items'], start=offset+1):
            track = item['track']
            search_query = f"{track['artists'][0]['name']} - {track['name']}"
            print(f"Processing track {index} of {spotify_playlist['tracks']['total']}: {search_query}")
            search_result = ytmusic.search(search_query, filter='songs')
            if search_result:
                ytmusic_track_ids.append(search_result[0]['videoId'])
            else:
                print(f"Track not found on YouTube Music: {search_query}")
        
        offset += len(spotify_tracks['items'])  # Update the offset for the next iteration
    
    # print how many tracks were found
    print(f"Found {len(ytmusic_track_ids)} of {spotify_playlist['tracks']['total']} tracks on YouTube Music")

    # Create a new playlist on YouTube Music
    print("Creating YouTube Music playlist...")
    playlist_id = ytmusic.create_playlist(spotify_playlist['name'], spotify_playlist['description'])    

    # Add tracks to the new YouTube Music playlist in chunks
    print("Adding tracks to YouTube Music playlist...")
    total = 0 
    for i, chunk in enumerate(chunkify(ytmusic_track_ids, chunk_size), start=1):
        # get the list of IDs from the playlist
        targetPl = ytmusic.get_playlist(playlist_id, limit=load_limit)
        # check if any tracks are already in the playlist, if so remove them from the chunk

        if deduplicate:
            try:
                for track in chunk:
                    if ContainsTrackId(track, targetPl['tracks']):
                        chunk.remove(track)
                        print(f"Track {track} already in playlist, skipping...")
            except:
                pass

        # add the chunk to the playlist
        print(f"Adding chunk {i}...")
        resp = ytmusic.add_playlist_items(playlist_id, chunk, duplicates=(not deduplicate))
        
        if debug:
            # print the response from YouTube Music
            print(resp)

        # count how many tracks were added
        for song in chunk:
            total += 1

        sleep(sleep_time)  # Prevent YouTube Music rate limiting
    
    # print how many tracks were added
    print(f"Added {total} tracks to YouTube Music playlist")

    print("Conversion complete!")

# Convert a Spotify playlist to a YouTube Music playlist
convert_playlist(playlis)
