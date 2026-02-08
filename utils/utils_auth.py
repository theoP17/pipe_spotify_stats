import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_spotify_client():
    cache_content = os.getenv('SPOTIPY_CACHE')
    cache_path = ".cache"
    if cache_content:
        with open(cache_path, "w") as f:
            f.write(cache_content)
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope="user-library-read",
        cache_path=cache_path,
        open_browser=False if cache_content else True
    ))

def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    json_path = 'google_creds.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    return gspread.authorize(creds)
