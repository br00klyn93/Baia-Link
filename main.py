from flask import Flask, request, render_template, redirect
from flask import make_response, Response

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

# For the indentifier retriever
import struct
import urllib.parse, urllib.request
import json


app = Flask(__name__)

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

playlists = sp.user_playlists('digitalageb')

pl_id = 'spotify:playlist:7lNJwcxRrS16RwyGhHfxLF'

itunes_identifiers = []

@app.route('/')
def main():
    return(get_spotify())


# On post request => get_spotify() then display()
def convert_itunes(title, artist):
    headers = {
        "X-Apple-Store-Front" : "143446-10,32 ab:rSwnYxS0 t:music2",
        "X-Apple-Tz" : "7200"
    }
    url = "https://itunes.apple.com/WebObjects/MZStore.woa/wa/search?clientApplication=MusicPlayer&term=" + urllib.parse.quote(title)
    request = urllib.request.Request(url, None, headers)

    try:
        response = urllib.request.urlopen(request)
        data = json.loads(response.read().decode('utf-8'))
        songs = [result for result in data["storePlatformData"]["lockup"]["results"].values() if result["kind"] == "song"]

        # Attempt to match by title & artist
        for song in songs:
            if song["name"].lower() == title.lower() and (song["artistName"].lower() in artist.lower() or artist.lower() in song["artistName"].lower()):
                return song["id"]

        # Attempt to match by title if we didn't get a title & artist match
        for song in songs:
            if song["name"].lower() == title.lower():
                return song["id"]

    except:
        # We don't do any fancy error handling.. Just return None if something went wrong
        return None



def get_spotify():
    song_ids = []
    artist_names = []

    we_out = []

    response = sp.playlist_tracks(pl_id,offset=0,fields='items.track.name,items.track.artists,total')
    for i in response['items']:
        ye = str(i)
        print("ye: ", ye.partition("type")[2].partition("name")[2])
        name = ye[10:].partition("type")[2]
        name = name.partition("name")[2]
        if name.find("name") != -1:
            name = name.partition("name")[2]
            name = name[4:-3]
            if name.find("name") != -1:
                name = name.partition("name")[2]
                name = name[4:-3]
        else:
            name = name[4:-3]

        artist = ye[22:].partition("name")[2]
        artist = artist[4:].partition("'")[0]

        if ye == '':
            continue
        else:
            song_ids.append(name)
            artist_names.append(artist)

    num = 0
    for i in song_ids:
        we_out.append(i+' '+artist_names[num])
        convert_itunes(i,artist_names[num])
        num+=1


    return(finish(we_out))

def finish(songids):
    print(itunes_identifiers)
    return("/".join(songids) + "-".join(itunes_identifiers))


if __name__ == "__main__":
    app.run("0.0.0.0",port=5000)
