import subprocess
import deezer
import time
import os
from dotenv import load_dotenv
load_dotenv()

print("Starting autodownload.py...")

while True:
    print("Logging in...")
    client = deezer.Client(access_token=os.environ.get("ACCESS_TOKEN"))

    print("Getting playlist...")
    playlist_tracks = client.get_playlist(int(os.environ.get("PLAYLIST_ID"))).tracks
    for track in playlist_tracks:
        print("Downloading " + track.artist.name + ", " + track.title + "...")
        subprocess.run(["python", "orpheus.py", "--output", os.environ.get("DL_LOCATION") + "/" + track.artist.name + "/" + track.album.title + "/", track.link], cwd="orpheusdl/")
        
        print("Deleting " + track.artist.name + ", " + track.title + "...")
        client.get_playlist(int(os.environ.get("PLAYLIST_ID"))).delete_tracks([track])
    
    print("Sleeping for 1 hour...")
    time.sleep(60)