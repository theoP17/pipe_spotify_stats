import pandas as pd

def extract_playlist_tracks(sp, playlist_id):
    # Fetch tracks from a specific playlist instead of "Liked Songs"
    results = sp.playlist_items(playlist_id, limit=50)
    tracks = []

    for item in results['items']:
        track = item['track']
        # Spotify returns None for podcast episodes or local files; we skip those
        if track is None:
            continue

        tracks.append({
            'Artist': track['artists'][0]['name'],
            'Track Name': track['name'],
            'Album': track['album']['name'],
            'Added At': item['added_at'],
            'Added By (ID)': item['added_by']['id'],
            'Spotify URL': track['external_urls']['spotify'],
            'Album Cover': track['album']['images'][0]['url']
        })
    return pd.DataFrame(tracks)

def upload_to_gsheet(client, sheet_name, df):
    sheet = client.open(sheet_name).sheet1
    # Convert DataFrame to list of lists for gspread
    data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
    sheet.clear()
    sheet.update('A1', data_to_upload)
