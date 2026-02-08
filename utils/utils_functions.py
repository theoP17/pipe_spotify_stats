import pandas as pd

def extract_saved_tracks(sp):
    results = sp.current_user_saved_tracks(limit=50)
    tracks = []
    for item in results['items']:
        track = item['track']
        tracks.append({
            'Artist': track['artists'][0]['name'],
            'Track Name': track['name'],
            'Album': track['album']['name'],
            'Added At': item['added_at']
        })
    return pd.DataFrame(tracks)

def upload_to_gsheet(client, sheet_name, df):
    sheet = client.open(sheet_name).sheet1
    data_to_upload = [df.columns.values.tolist()] + df.values.tolist()
    sheet.clear()
    sheet.update('A1', data_to_upload)
