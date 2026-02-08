🎵 Spotify Stats Pipeline
📖 Context & General Overview
This project is an automated ETL (Extract, Transform, Load) pipeline that syncs your personal Spotify "Saved Tracks" into a Google Sheet. It is designed for users who want to track their listening habits or archive their music library without manual work.

The system is built with Python and utilizes GitHub Actions to run as a "headless" service, meaning it executes in the cloud every day at a scheduled time (9:00 AM UTC) without needing your computer to be turned on.

🏗 Project Architecture
The project is modularized to ensure security, maintainability, and scalability.

File Structure:

main.py: The central "brain" of the project. It coordinates the authentication, data fetching, and uploading processes.

utils/utils_auth.py: Handles all API handshakes. It manages the Spotify OAuth2 flow (including the .cache token for headless environments) and Google Service Account authentication.

utils/utils_functions.py: Contains the data logic. It extracts JSON from Spotify, transforms it into a cleaned Pandas DataFrame, and handles the Google Sheets API push.

.github/workflows/main.yml: The automation engine. It defines the environment, installs dependencies, injects GitHub Secrets, and schedules the script.

requirements.txt: Lists all necessary Python libraries (spotipy, gspread, pandas, etc.).

⚙️ How the Script Works
Headless Auth: On GitHub, the script looks for a secret called SPOTIPY_CACHE. It writes this to a local .cache file, tricking the Spotify API into thinking a user has already logged in via a browser.

Extraction: The script calls the Spotify API to retrieve the 50 most recently saved tracks.

Data Cleaning: It parses the complex JSON response to pull out:

Artist Name

Track Name

Album Title

Added Date

Google Sheet Update: Using the gspread library, the script connects to your pre-existing sheet, clears the old data, and replaces it with the fresh list of tracks starting from cell A1.

🚀 Future Roadmap & Improvements
To take this from a personal script to a production-grade data tool, the following enhancements are proposed:

1. API-First Architecture

The Idea: Wrap the script in a FastAPI or Flask wrapper.

How to do it: Deploy the code to a platform like Heroku or AWS Lambda. Instead of a timer, you could trigger the sync via a URL or a mobile app button.

2. Relational Data Storage

The Idea: Replace (or supplement) Google Sheets with a PostgreSQL database.

How to do it: Use SQLAlchemy to store every sync event.

Benefit: This allows you to perform "Time Series" analysis, such as seeing how your taste in genres changes month-over-month, which is difficult in a flat sheet that is constantly overwritten.

3. Audio Feature Enrichment

The Idea: Pull deep metadata for every song.

How to do it: Add a function to query Spotify's /audio-features endpoint.

Data Points: Add columns for BPM (Tempo), Energy, Danceability, and Acousticness. You could then auto-generate "Workout" or "Chill" sheets based on these scores.

4. Multi-User Support (SaaS Model)

The Idea: Allow others to use your tool.

How to do it: Implement a full OAuth2 "Login with Spotify" flow and store multiple users' tokens in an encrypted database.