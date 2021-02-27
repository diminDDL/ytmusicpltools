from ytmusicapi import YTMusic
import json

ytmusic = YTMusic('headers_auth.json') #read auth file
songs = ytmusic.get_liked_songs(limit=5000)

targetId = input("Plese enter playlist ID to add liked songs: ")
print(targetId + " Will be used as target playlist")

targetPl = ytmusic.get_playlist(targetId, limit=5000)

def ContainsTrackId (TrackId, TrackDict):
    for i in TrackDict:
        if i['videoId'] == TrackId:
            return True
    return False

songList = []
for n in songs['tracks']:
    if not ContainsTrackId(n['videoId'], targetPl['tracks']):
        print("not in playlist: " + n['videoId'])
        songList.append(n['videoId'])
    else:
        print("in playlist already: " + n['videoId'])
print(songList)
print(json.dumps(ytmusic.add_playlist_items(targetId,videoIds = songList, duplicates=True)))
