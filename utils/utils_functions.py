import pandas as pd
import requests
from datetime import datetime

def extract_playlist_tracks(sp, playlist_id):
    # 1. Get the access token
    token = sp.auth_manager.get_access_token(as_dict=False)

    # 2. Call the /items endpoint
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/items"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"limit": 50, "additional_types": "track"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Spotify API Error: {response.status_code} - {response.text}")

    results = response.json()
    tracks = []
    user_names = {} # Cache to store IDs and their Pseudos

    for item in results.get('items', []):
        track = item.get('track')
        if not track: continue

        # Get the ID of the person who added the track
        user_id = item.get('added_by', {}).get('id')

        # If we haven't looked up this user's pseudo yet, do it now
        if user_id not in user_names:
            try:
                user_profile = sp.user(user_id)
                user_names[user_id] = user_profile.get('display_name') or user_id
            except:
                user_names[user_id] = user_id # Fallback to ID if lookup fails

        tracks.append({
            'Artist': track['artists']['name'],
            'Track Name': track['name'],
            'Album': track['album']['name'],
            'Added At': item.get('added_at'),
            'Added By': user_names[user_id],
            'Spotify URL': track['external_urls'].get('spotify')
        })

    return pd.DataFrame(tracks)

def upload_to_gsheet(client, sheet_name, df):
    sh = client.open(sheet_name)

    try:
        # Static target: 'Extract'
        worksheet = sh.worksheet('Extract')
    except:
        worksheet = sh.add_worksheet(title='Extract', rows=100, cols=20)
        print("Created missing 'Extract' tab.")

    data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
    worksheet.clear()
    worksheet.update('A1', data_to_upload)
