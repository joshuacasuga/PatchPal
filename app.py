import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, url_for, session, redirect, render_template
#url_for formats urls for us so we don't have to hardcode all of our urls
#session creates sessions for our user
#render_template is for our flask templates
from requests import post
import json
import base64


USER_TOKEN = "token_info"
AHA_CPR_PLAYLIST_ID = "2mU2FNAhSOtQwW0hBgQMaK"
AHA_CPR_PLAYLIST_URL = "https://api.spotify.com/v1/playlists/" + AHA_CPR_PLAYLIST_ID
AHA_CPR_PLAYLIST_TRACKS = AHA_CPR_PLAYLIST_URL + "/tracks"
app = Flask(__name__)

#for getting authentication for spotify!
def creating_spotify_oauth():
    return SpotifyOAuth(
        client_id = os.getenv("CLIENT_ID"),
        client_secret = os.getenv("CLIENT_SECRET"),
        redirect_uri = url_for("redirect", _external = True),
        scope = "user-top-read user-library-read" #scope is what is requested from our user
    )

def get_user_token():
     token_info = session.get(USER_TOKEN, None)
     return token_info

@app.route('/cpr_songs')
def cpr_songs():

    return render_template('cpr_songs.html')

@app.route('/login')
def login():
        sp_oauth = creating_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

@app.route('/redirect')
def redirect():
      #continues
      sp_oauth = creating_spotify_oauth()
      session.clear()
      code = request.args.get('code')
      token_info = sp_oauth.get_access_token(code)
      session[USER_TOKEN] = token_info
      return redirect(url_for("cpr_songs", _external = True))




#spotify_ID for the American Heart Association's CPR playlist: 2mU2FNAhSOtQwW0hBgQMaK
def call_AHA_playlist():   #this offers the user the AHA cpr official playlist
    user_token = get_user_token()
    sp = spotipy.Spotify(
         auth = user_token['access_token']
    )
    AHA_playlist = sp.playlist(AHA_CPR_PLAYLIST_ID, fields=None, market=None, additional_types=('track',))
    return AHA_playlist


#def user_cpr_songs():   #this suggests songs that the user has played w/100-12o bpm for cpr
 #   user_token = get_user_token()
 #   sp = spotipy.Spotify(
  #       auth = user_token['access_token']
   # )
    #AHA_playlist = sp.playlist(AHA_CPR_PLAYLIST_ID, fields=None, market=None, additional_types=('track',))
    #AHA_tracks = sp.playlist_tracks(AHA_CPR_PLAYLIST_ID, fields=None, limit=20, offset=0, market=None, additional_types=('track',))
    #return AHA_playlist
      
      
      

