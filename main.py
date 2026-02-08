import os
from dotenv import load_dotenv
from utils.utils_auth import get_spotify_client, get_gspread_client
from utils.utils_functions import extract_saved_tracks, upload_to_gsheet

load_dotenv()

def main():
    print("THEO EST UN GROS CON")
    try:
        print("Connecting to APIs...")
        sp = get_spotify_client()
        gs = get_gspread_client()
        print("Extracting Spotify data...")
        df = extract_saved_tracks(sp)
        print(f"Updating Google Sheet: {os.getenv('GOOGLE_SHEET_NAME')}...")
        upload_to_gsheet(gs, os.getenv('GOOGLE_SHEET_NAME'), df)
        print("Automation Successful!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main() 
