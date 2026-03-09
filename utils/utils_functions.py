import pandas as pd
import requests
from datetime import datetime

def extract_playlist_tracks(sp, playlist_id):
    # 1. Get the access token from your existing spotipy client
    token = sp.auth_manager.get_access_token(as_dict=False)

    # 2. Use the new /items endpoint manually as per the Spotify update
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/items"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 50, "additional_types": "track"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        raise Exception(f"Spotify API Error: {response.status_code} - {response.text}")

    results = response.json()
    tracks = []

    for item in results.get('items', []):
        track = item.get('track')
        if not track: continue

        tracks.append({
            'Artist': track['artists'][0]['name'],
            'Track Name': track['name'],
            'Album': track['album']['name'],
            'Added At': item.get('added_at'),
            'Added By (ID)': item.get('added_by', {}).get('id'),
            'Spotify URL': track['external_urls'].get('spotify'),
            'Album Cover': track['album']['images'][0]['url'] if track['album']['images'] else None
        })

    return pd.DataFrame(tracks)

def upload_to_gsheet(client, sheet_name, df):
    sh = client.open(sheet_name)

    # Get the current ISO week number
    week_name = f"Week {datetime.now().isocalendar()[1]}"

    try:
        # Check if tab exists
        worksheet = sh.worksheet(week_name)
    except:
        # Create it if it's a new week
        worksheet = sh.add_worksheet(title=week_name, rows=100, cols=20)
        print(f"Successfully created new tab for: {week_name}")

    data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
    worksheet.clear()
    worksheet.update('A1', data_to_upload)
