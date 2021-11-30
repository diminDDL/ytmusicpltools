from ytmusicapi import YTMusic
import os
import time

ytmusic = YTMusic('headers_auth.json') #read auth file
songs = ytmusic.get_liked_songs(limit=5000)

f = open("IdList.txt", "r")
IdList = f.read()
f.close()
#print("the downloaded Ids will be listed below:")
#print(IdList)
#print(type(IdList))
#print(os.path.abspath("youtube-dl.exe"))

q = len(songs['tracks'])
q -= 1
while(q >= 0):
    n = songs['tracks'][q]
    print("Current video Id: " + n['videoId'])
    print("Current track Id: " +  str(q))
    if n['videoId'] not in IdList:
        print("Not downloaded previously, downloading...")
        IdList += n['videoId']
        IdList += "\n"
        os.system('{} --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata --metadata-from-title "(?P<artist>.+?) - (?P<title>.+)" --output "./dl/%(creator)s - %(title)s.%(ext)s" https://www.youtube.com/watch?v={}'.format(os.path.abspath("youtube-dl"),n['videoId']))
        time.sleep(1)
        f = open("IdList.txt", "w")
        f.seek(0)
        f.write(IdList)
        f.truncate()
    q -= 1

# for n in songs['tracks']:
#     print("Current video Id: " + n['videoId'])
#     #print("Current track Id: " +  n[''])
#     if n['videoId'] not in IdList:
#         print("Not downloaded previously, downloading...")
#         IdList += n['videoId']
#         IdList += "\n"
#         os.system('{} --extract-audio --audio-format mp3 --audio-quality 0 --embed-thumbnail --add-metadata --metadata-from-title "(?P<artist>.+?) - (?P<title>.+)" --output "dl\%(creator)s - %(title)s.%(ext)s" https://www.youtube.com/watch?v={}'.format(os.path.abspath("youtube-dl.exe"),n['videoId']))
#         time.sleep(1)
#         f = open("IdList.txt", "w")
#         f.seek(0)
#         f.write(IdList)
#         f.truncate()
