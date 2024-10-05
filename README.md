# Deezer Trending to YouTube Downloader

This project retrieves the trending tracks from **Deezer** based on the genre of the day and searches for equivalent music videos on **YouTube**. It then uses **yt-dlp** to download and convert these tracks into the desired audio format (default: `mp3`).

## Features
- Automatically fetches the trending tracks from Deezer based on the day of the week.
- Searches YouTube for the corresponding music videos of those tracks.
- Downloads and converts the videos from YouTube to audio files using **yt-dlp**.

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

## Usage

1. Clone this repository.
2. Install the required libraries listed above.
3. Run the script:
   ```bash
   python main.py
   ```

The script will automatically fetch the trending Deezer tracks, search for their YouTube equivalents, and download them as audio files.

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
- Foreach day of the week, you can update which style you prefer for each day.
