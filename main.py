from flask import Flask, request, render_template, redirect
from flask import make_response, Response

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

app = Flask(__name__)

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

playlists = sp.user_playlists('digitalageb')

pl_id = 'spotify:playlist:02ffdMW3wCP6CWLXtKh7vb'

song_ids = []

@app.route('/')
def main():
    get_spotify()
    return(display())

# On post request => get_spotify() then display()

def get_spotify():
    response = sp.playlist_tracks(pl_id,offset=0,fields='items.track.name,total')
    for i in response['items']:
        ye = str(i)
        ye = ye[:-3]

        if ye == '':
            continue
        else:
            song_ids.append(ye)
            print(ye)
            
    offset=0
    offset = offset + len(response['items'])
    print("offset: ", offset, "/", response['total'])

    if len(response['items']) == 0:
        break


def display():
    return("\n".join(song_ids))


if __name__ == "__main__":
    app.run("0.0.0.0",port=5000)
