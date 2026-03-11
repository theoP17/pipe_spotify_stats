import pandas as pd
import spotipy

def extract_playlist_tracks(sp, playlist_id):
    try:
        # USE THIS: This automatically attaches the Bearer Token
        results = sp.playlist_items(playlist_id)

        tracks = []
        for item in results.get('items', []):
            track = item.get('track')
            if not track or not track.get('name'):
                continue

            tracks.append({
                'Artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                'Track Name': track['name'],
                'Album': track['album']['name'],
                'Added At': item.get('added_at'),
                'Added By (ID)': item.get('added_by', {}).get('id', 'Unknown'),
                'Spotify URL': track['external_urls'].get('spotify', '')
            })

        return pd.DataFrame(tracks)

    except spotipy.exceptions.SpotifyException as e:
        # This will catch 403s and 401s and tell you exactly why
        print(f"❌ Spotify API Error: {e.http_status} - {e.msg}")
        return pd.DataFrame()

def upload_to_gsheet(client, spreadsheet_id, df):
    if df.empty:
        print("No data extracted.")
        return

    # 1. Opening the sheet:
    # If spreadsheet_id is the long alphanumeric string in the URL, use open_by_key
    # If it's the actual Title, use open()
    sh = client.open_by_key(spreadsheet_id)

    try:
        worksheet = sh.worksheet('Extract')
    except:
        # Note: rows and cols must be integers, not strings
        worksheet = sh.add_worksheet(title='Extract', rows=1000, cols=20)

    # 2. Prepare data
    # We replace NaN with empty strings and convert everything to string
    # to avoid JSON serialization errors with dates or None types.
    df_clean = df.fillna("").astype(str)
    data_to_upload = [df_clean.columns.values.tolist()] + df_clean.values.tolist()

    # 3. Execution
    worksheet.clear()

    # Using 'value_input_option' is crucial for ensuring dates/numbers
    # are treated correctly by Google Sheets logic.
    worksheet.update('A1', data_to_upload, value_input_option='RAW')
    print("✅ Google Sheet 'Extract' tab updated!")
