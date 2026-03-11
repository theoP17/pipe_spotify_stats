import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_spotify_client():
    cache_path = ".cache"

    # Check if file exists, if so, delete it to force a fresh login
    if os.path.exists(cache_path):
        os.remove(cache_path)
        print("🗑️ Old cache deleted to force new login.")

    auth_manager = SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
        scope="user-library-read playlist-read-private playlist-read-collaborative",
        cache_path=cache_path,
        open_browser=True,
        show_dialog=True  # This forces the window to pop up!
    )

    return spotipy.Spotify(auth_manager=auth_manager)

def get_gspread_client():
    # Updated to modern gspread scope
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

    # Ensure this path exists in your GitHub Repo or is provided via Secret
    json_path = '.creds/google_creds.json'

    if not os.path.exists(json_path):
        # Fallback if you are using a GitHub Secret for Google JSON
        import tempfile
        google_json = os.getenv('GOOGLE_CREDS_JSON')
        if google_json:
            with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
                tmp.write(google_json)
                json_path = tmp.name

    creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    return gspread.authorize(creds)
