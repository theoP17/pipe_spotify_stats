# 🎵 Spotify Stats Pipeline

## 📖 Context & General Overview
This project is an automated **ETL (Extract, Transform, Load)** pipeline that synchronizes your personal Spotify "Saved Tracks" into a Google Sheet. It is designed to provide a seamless way to archive music libraries and analyze listening habits without manual intervention.

The system is built with **Python** and utilizes **GitHub Actions** to operate as a "headless" service. It executes in the cloud on a daily schedule (9:00 AM UTC), ensuring your data is always up-to-date even if your local machine is offline.

---

## 🏗 Project Architecture
The project follows a modular design pattern to ensure security, maintainability, and clear separation of concerns.



### File Structure:
* **`main.py`**: The entry point of the application. It orchestrates the workflow by calling authentication and data processing modules.
* **`utils/utils_auth.py`**: Manages all API handshakes. It handles Spotify OAuth2 (including `.cache` token injection for cloud environments) and Google Service Account credentials.
* **`utils/utils_functions.py`**: Contains the core logic. It extracts raw JSON from Spotify, transforms it into a cleaned **Pandas DataFrame**, and manages the Google Sheets API push.
* **`.github/workflows/main.yml`**: The CI/CD engine. It defines the virtual environment, installs dependencies from `requirements.txt`, and safely injects GitHub Secrets into the execution.
* **`.gitignore`**: Critical security file that ensures local secrets (`.env`, `google_creds.json`) are never uploaded to the public repository.

---

## ⚙️ How the Script Works

1.  **Headless Authentication**: Since GitHub Actions cannot open a browser, the script uses a pre-generated `SPOTIPY_CACHE` secret. It writes this to a local file at runtime, allowing Spotify to verify the session automatically.
2.  **Data Extraction**: The script queries the Spotify Web API to retrieve the 50 most recently "Liked" or saved tracks.
3.  **Data Transformation**: It parses the nested JSON response into a flat structure containing:
    * **Artist Name**
    * **Track Name**
    * **Album Title**
    * **Added Date**
4.  **Google Sheets Synchronization**: Using the `gspread` library, the script opens the target spreadsheet, clears existing rows to prevent duplicates, and performs a bulk update with the new dataset.

---

## 🚀 Future Roadmap & Improvements

To evolve this from a personal automation script into a production-grade data product, the following improvements are recommended:

### 1. REST API Architecture
* **The Concept**: Wrap the logic in a **FastAPI** or **Flask** framework.
* **Implementation**: Deploy to a platform like AWS Lambda. This would allow you to trigger a sync via a web hook or a custom "Sync Now" button on a dashboard.

### 2. Advanced Data Storage (Relational Database)
* **The Concept**: Move from Google Sheets to a database like **PostgreSQL**.
* **Implementation**: Use an ORM like **SQLAlchemy** to "Upsert" data. 
* **Benefit**: This enables historical trend analysis (e.g., "Top genres of 2025") which is difficult when data is overwritten in a flat spreadsheet.

### 3. Audio Feature Enrichment
* **The Concept**: Enhance the dataset with Spotify's deep metadata.
* **Implementation**: Call the `/audio-features` endpoint for each track ID.
* **New Columns**: Add **BPM (Tempo)**, **Energy**, **Danceability**, and **Valence**. This allows for mood-based filtering directly within the sheet.

### 4. Containerization
* **The Concept**: Use **Docker** to package the application.
* **Implementation**: Create a `Dockerfile` to ensure the environment (Python version and OS libraries) is identical across local development and GitHub Actions.

---