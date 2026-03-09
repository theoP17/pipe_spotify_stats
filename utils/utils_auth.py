import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_spotify_client():
    # Only write to .cache if the environment variable (GitHub Secret) exists
    cache_content = os.getenv('SPOTIPY_CACHE')
    cache_path = ".cache"

    if cache_content:
        with open(cache_path, "w") as f:
            f.write(cache_content)

    # Initialize OAuth with the required scopes
    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope = "user-library-read playlist-read-private user-read-private",
        cache_path=cache_path,
        show_dialog=True
    )

    return spotipy.Spotify(auth_manager=auth_manager)

def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    json_path = '.creds/google_creds.json'
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    return gspread.authorize(creds)
