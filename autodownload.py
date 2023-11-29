import subprocess
import deezer
import time
import os
import json
import glob
from dotenv import load_dotenv
load_dotenv()

print("Starting autodownload.py...")

while True:
    print("Logging in...")
    client = deezer.Client(access_token=os.environ.get("ACCESS_TOKEN"))

    # Deezer download
    print("Getting deezer playlist...")
    playlist_tracks = client.get_playlist(int(os.environ.get("PLAYLIST_ID"))).tracks
    for track in playlist_tracks:
        print("Downloading " + track.artist.name + ", " + track.title + "...")
        subprocess.run(["python", "orpheus.py", "--output", os.environ.get("DL_LOCATION") + "/" + track.artist.name + "/" + track.album.title + "/", track.link], cwd="orpheusdl/")
        
        print("Deleting " + track.artist.name + ", " + track.title + "...")
        client.get_playlist(int(os.environ.get("PLAYLIST_ID"))).delete_tracks([track])
    
    # Youtube download
    print("Getting youtube playlist...")
    yt_json = json.loads(subprocess.run(["yt-dlp", "-J", "-s", "-q", "https://www.youtube.com/playlist?list=" + os.environ.get("YT_PLAYLIST_ID")], capture_output=True).stdout.decode("utf-8"))
    for video in yt_json["entries"]:
        # If the video isn't a music video
        if (video["album"] == None or video["artist"] == None or video["track"] == None):
            # If the video has already been downloaded, skip it
            if (glob.glob(os.environ.get("DL_LOCATION") + "/" + video["channel"] + "/" + video["title"] + ".*")):
                continue

            # Download the video
            print("Downloading " + video["channel"] + ", " + video["title"] + "...")
            subprocess.run(["yt-dlp", "-x", "-P", os.environ.get("DL_LOCATION"), "-o", "%(channel)s/%(title)s.%(ext)s", video["webpage_url"]])
        
        # If the video is a music video
        else:
            # If the video is already on deezer, download it from there
            search = client.search(artist=video["artist"], album=video["album"], track=video["track"])
            if len(search) == 0:
                # If the video has already been downloaded, skip it
                if (glob.glob(os.environ.get("DL_LOCATION") + "/" + video["artist"] + "/" + video["album"] + "/" + video["track"] + ".*")):
                    continue

                print("Downloading " + video["artist"] + ", " + video["track"] + "...")
                subprocess.run(["yt-dlp", "-x", "-P", os.environ.get("DL_LOCATION"), "-o", "%(artist)s/%(album)s/%(track)s.%(ext)s", video["webpage_url"]])
            else:
                # If the video has already been downloaded, skip it
                if (glob.glob(os.environ.get("DL_LOCATION") + "/" + search[0].artist.name + "/" + search[0].album.title + "/" + search[0].title + ".*")):
                    continue
                
                print("Downloading " + search[0].artist.name + ", " + search[0].title + "...")
                subprocess.run(["python", "orpheus.py", "--output", os.environ.get("DL_LOCATION") + "/" + search[0].artist.name + "/" + search[0].album.title + "/", search[0].link], cwd="orpheusdl/")

    print("Sleeping for 1 hour...")
    print("")
    time.sleep(3600)