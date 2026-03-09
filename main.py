import os
from dotenv import load_dotenv
from utils.utils_auth import get_spotify_client, get_gspread_client
# Update the import to match the new function name
from utils.utils_functions import extract_playlist_tracks, upload_to_gsheet

load_dotenv()

def main():
    try:
        # 1. Get credentials from .env
        sheet_name = os.getenv('GOOGLE_SHEET_NAME')
        playlist_id = os.getenv('SPOTIFY_PLAYLIST_ID')

        if not playlist_id:
            raise ValueError("SPOTIFY_PLAYLIST_ID not found in .env file")

        print("Connecting to APIs...")
        sp = get_spotify_client()
        gs = get_gspread_client()

        print(f"Extracting tracks from playlist ID: {playlist_id}...")
        # Use the new playlist extraction function
        df = extract_playlist_tracks(sp, playlist_id)

        print(f"Updating Google Sheet: {sheet_name}...")
        upload_to_gsheet(gs, sheet_name, df)

        print("Automation Successful!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
