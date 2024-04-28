import os
from dotenv import load_dotenv
from openai import OpenAI
from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv(".env")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
USER_TOKEN = "token_info"
AHA_CPR_PLAYLIST_ID = "2mU2FNAhSOtQwW0hBgQMaK"
AHA_CPR_PLAYLIST_URL = "https://api.spotify.com/v1/playlists/" + AHA_CPR_PLAYLIST_ID
AHA_CPR_PLAYLIST_TRACKS = AHA_CPR_PLAYLIST_URL + "/tracks"
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_NAME'] = 'KKMJ'
if __name__ == "__main__":
    app.run(debug=True)

api = OpenAI(api_key=OPENAI_API_KEY)

def get_response(user_input):
    response = api.chat.completions.create(
        model="ft:gpt-3.5-turbo-0125:personal:firstaidmodel16:9Il0mv2b:ckpt-step-116",
        messages=[
            {"role": "system", "content": "Act as a nurse who gives suggestions for first aid."},
            {"role": "user", "content": user_input}
        ])
    return response.choices[0].message.content

def creating_spotify_oauth():
    return SpotifyOAuth(
        client_id = os.getenv("CLIENT_ID"),
        client_secret = os.getenv("CLIENT_SECRET"),
        redirect_uri = url_for("redirect_page", _external = True),
        scope = "user-top-read user-library-read" #scope is what is requested from our user
    )

def get_user_token():
     token_info = session.get(USER_TOKEN, None)
     return token_info

#spotify_ID for the American Heart Association's CPR playlist: 2mU2FNAhSOtQwW0hBgQMaK
def call_AHA_playlist():   #this offers the user the AHA cpr official playlist
    user_token = get_user_token()
    sp = spotipy.Spotify(
         auth = user_token['access_token']
    )
    AHA_playlist = sp.playlist(AHA_CPR_PLAYLIST_ID, fields=None, market=None, additional_types=('track',))
    return AHA_playlist

#we first get top tracks of user for the seed_ids as the seed_tracks the fuction bases it off of
def get_top_tracks():
    user_token = get_user_token()
    sp = spotipy.Spotify(
        auth = user_token['access_token']
    )
    top_tracks = sp.current_user_top_tracks(limit=5)
    return top_tracks
     
#we use the get recommendations endpoint to get tracks between the bpm 100-120.
def user_cpr_songs():   #this suggests songs that the user has played w/100-12o bpm for cpr
    user_token = get_user_token()
    sp = spotipy.Spotify(
         auth = user_token['access_token']
    )
    curr_user_top = get_top_tracks()
    recommended_cpr_songs = sp.recommendations(
        seed_tracks = [track['id'] for track in curr_user_top['items']],
        limit = 10,
        country = None,
        min_tempo = 100,
        max_tempo = 120
    )
    return recommended_cpr_songs

@app.route('/')
def index():
    return render_template('index.html', title="First Aid")

@app.route('/result', methods=['POST'])
def get_result():
    query = request.form['search_query']
    response = get_response(query)
    #result = response.choices[0].message.content
    return render_template('result.html', query=query, result=response)

@app.route('/firstaid')
def first_aid():
    return render_template('firstaid.html')

@app.route('/cpr')
def cpr():
    return render_template('cpr.html')

@app.route('/hotlines')
def hotlines():
    return render_template('hotlines.html')

@app.route('/login')
def login():
        sp_oauth = creating_spotify_oauth()
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

@app.route('/redirect_page')
def redirect_page():
      #continues
      sp_oauth = creating_spotify_oauth()
      session.clear()
      code = request.args.get('code')
      token_info = sp_oauth.get_access_token(code)
      session[USER_TOKEN] = token_info
      return redirect(url_for("cpr_songs", _external = True))

@app.route('/cpr_songs')
def cpr_songs():
    aha_playlist = call_AHA_playlist()
    user_songs = user_cpr_songs()
    return render_template('cpr_songs.html', aha_playlist=aha_playlist, user_songs=user_songs)

#user_input = input()
#print(get_response(user_input))