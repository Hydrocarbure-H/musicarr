# Musicarr

This project retrieves the trending tracks from **Deezer** based on the genre of the day and searches for equivalent music videos on **YouTube**. It then uses **yt-dlp** to download and convert these tracks into the desired audio format (default: `mp3`). Additionally, the script keeps track of downloaded tracks to avoid downloading the same track multiple times.

**Disclaimer:**

This project is for educational purposes only. It is designed to demonstrate how to interact with APIs (Deezer, YouTube) and download media using publicly available tools like **yt-dlp**. Please be aware of and comply with all copyright laws and the terms of service of the platforms you are interacting with. Unauthorized downloading of copyrighted content may violate these terms and could result in legal consequences. Use this project responsibly and respect the rights of content creators.

## Features
- Automatically fetches the trending tracks from Deezer based on the day of the week.
- Searches YouTube for the corresponding music videos of those tracks.
- Downloads and converts the videos from YouTube to audio files using **yt-dlp**.
- **Download history tracking**: The script maintains a history of previously downloaded tracks, ensuring that duplicate downloads are avoided.

## Requirements

To run this project, you need the following:

- **Python 3.x**
- **yt-dlp**: A powerful downloader for media from various platforms.
- **youtube_search**: A Python library to search YouTube videos.

### Install Requirements

You can install the required libraries using the following command:

```bash
pip3 install -r requirements.txt
```

## How It Works

1. **Get Deezer Trending Tracks**: The script uses the Deezer API to fetch the trending tracks for a specific genre based on the current day of the week.
2. **Search for YouTube Videos**: For each track retrieved from Deezer, it searches for the corresponding video on YouTube using the **youtube_search** library.
3. **Download the Track**: The script then uses **yt-dlp** to download the audio from YouTube, convert it to the specified format (default: `mp3`), and store it locally.
4. **Track Download History**: The script maintains a JSON file that logs previously downloaded tracks. If a track has already been downloaded, it will be skipped in future executions, ensuring that no duplicate downloads occur.

## Usage

1. Clone this repository.
2. Install the required libraries listed above.
3. Run the script:
   ```bash
   python main.py
   ```

The script will automatically fetch the trending Deezer tracks, search for their YouTube equivalents, and download them as audio files while avoiding duplicates using the download history.

## Example

The script will output something like this:

```
Downloading track: Shape of You by Ed Sheeran
Successfully downloaded and converted https://www.youtube.com/abc123
Downloading track: Blinding Lights by The Weeknd
Successfully downloaded and converted https://www.youtube.com/def456
```

## Customization

- You can adjust the **audio format** or **quality** by modifying the `download_with_ytdlp()` function.
- You can set the number of tracks to retrieve by changing the `limit` parameter in `get_deezer_genre_tracks()`.
- The **download history** is stored in a JSON file and can be manually edited if necessary.
- You can update the genres for each day of the week in the `get_genre_id()` function to customize the types of music fetched from Deezer.