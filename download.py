import sys
import subprocess
import deezer
import os
from dotenv import load_dotenv
load_dotenv()

client = deezer.Client()
songname = " ".join(sys.argv[1:])
search_results = client.search(query=songname)

index = 0
for track in search_results[:10]:
    print("[" + str(index) + "] " + track.artist.name + ", " + track.album.title + ", " + track.title)
    index += 1

track_number = input('Track number: ')
track = search_results[int(track_number)]
print("DOWNLOADING: " + track.artist.name + ", " + track.album.title + ", " + track.title)

subprocess.run(["python", "orpheus.py", "--output", os.environ.get("DL_LOCATION") + "/" + track.artist.name + "/" + track.album.title + "/", track.link], cwd="orpheusdl/")