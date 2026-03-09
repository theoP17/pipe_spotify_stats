# 🎵 Spotify Playlist Tracker to Google Sheets

This automation extracts track metadata from a specific **private or collaborative Spotify playlist** and archives it into a **Google Sheet**. It is built to bypass recent 2026 API restrictions and organizes data by creating a new tab for each **ISO week**.

---

## 🚀 Key Features

* **Manual API Request**: Bypasses the 2026 `/tracks` endpoint deprecation by hitting the `/items` endpoint directly via the `requests` library.
* **Collaborative Tracking**: Captures "Added By" data, allowing you to see exactly which user contributed which track to the playlist.
* **Weekly Archiving**: Automatically detects the current ISO week number and either updates or creates a dedicated tab (e.g., `Week 11`).
* **Security Guard**: Implements a strict security protocol to ensure `.env`, `.cache`, and `google_creds.json` are never pushed to public repositories.

---

## 🛠️ Setup Instructions

### 1. Spotify API Configuration
1.  Create an application in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
2.  **Required**: Add your Spotify email address under **Settings > User Management** to allow access while in Development Mode.
3.  Set your Redirect URI to `http://127.0.0.1:8888/callback`.

### 2. Google Sheets API Configuration
1.  Enable the **Google Sheets** and **Google Drive** APIs in the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a Service Account, download the JSON key, and save it in the root folder as `google_creds.json`.
3.  Share your target Google Sheet with the Service Account's email address (found in the JSON).

### 3. Environment Variables (`.env`)
Create a `.env` file in the root directory with the following content:
```text
SPOTIPY_CLIENT_ID='your_spotify_client_id'
SPOTIPY_CLIENT_SECRET='your_spotify_client_secret'
SPOTIPY_REDIRECT_URI='[http://127.0.0.1:8888/callback](http://127.0.0.1:8888/callback)'
SPOTIFY_PLAYLIST_ID='your_playlist_id'
GOOGLE_SHEET_NAME='Stats Spotify'
