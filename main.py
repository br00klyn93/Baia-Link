from flask import Flask, request, render_template, redirect
from flask import make_response, Response

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

app = Flask(__name__)

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

playlists = sp.user_playlists('digitalageb')

pl_id = 'spotify:playlist:02ffdMW3wCP6CWLXtKh7vb'

@app.route('/')
def main():
    return(get_spotify())
    

# On post request => get_spotify() then display()

def get_spotify():
    song_ids = []
    artist_names = []
    
    we_out = []
    
    response = sp.playlist_tracks(pl_id,offset=0,fields='items.track.name,items.track.artists,total')
    for i in response['items']:
        ye = str(i)
        print("ye: ", ye)
        name = ye.partition("type")[2]
        name = name.partition("name")[2]
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
        we_out.append(i+'-'+artist_names[num])
        num+=1
    
    return(display(we_out))


def display(songids):
    return("/".join(songids))


if __name__ == "__main__":
    app.run("0.0.0.0",port=5000)
