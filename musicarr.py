import json
import os
import requests
import datetime
import subprocess
from typing import List, Dict, Any
from youtube_search import YoutubeSearch

DOWNLOAD_HISTORY_FILE = "./download_history.json"
DESTINATION_FOLDER = "./musicarr_downloads"


def load_download_history() -> List[Dict[str, Any]]:
    """
    Loads the download history from the JSON file.

    :return: List of previously downloaded tracks.
    """
    try:
        with open(DOWNLOAD_HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        os.system("echo {} > " + DOWNLOAD_HISTORY_FILE)
        return []


def save_download_history(downloaded_tracks: List[Dict[str, Any]]):
    """
    Saves the download history to the JSON file.

    :param downloaded_tracks: List of tracks to save.
    """
    # Get the existing download history
    existing_history = load_download_history()
    
    # Append the new tracks to the existing history
    downloaded_tracks.extend(existing_history)
    
    with open(DOWNLOAD_HISTORY_FILE, "w") as f:
        json.dump(downloaded_tracks, f)


def filter_new_tracks(
    trending_tracks: List[Dict[str, Any]],
    download_history: List[Dict[str, Any]],
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Filters out already downloaded tracks and returns a list of new tracks to download.

    :param trending_tracks: List of trending tracks from Spotify.
    :param download_history: List of previously downloaded tracks.
    :param limit: The number of new tracks to download.
    :return: List of new tracks to download.
    """
    downloaded_set = {(track["title"], track["artist"]) for track in download_history}
    new_tracks = [
        track
        for track in trending_tracks
        if (track["title"], track["artist"]) not in downloaded_set
    ]
    return new_tracks[:limit]


def get_genre_id() -> int:
    """
    Returns the genre ID based on the current day of the week.

    :return: Genre ID corresponding to the current day.
    """
    genres: Dict[str, int] = {
        "Monday": 132,  # Pop
        "Tuesday": 152,  # Rock
        "Wednesday": 116,  # Hip Hop
        "Thursday": 129,  # Jazz
        "Friday": 113,  # Dance
        "Saturday": 197,  # K-Pop
        "Sunday": 106,  # Electro
    }

    # Get the current day of the week
    current_day: str = datetime.datetime.now().strftime("%A")

    # Return the genre ID based on the day of the week
    return genres.get(current_day)


def get_deezer_genre_tracks(limit: int = 50, index: int = 0) -> List[Dict[str, Any]]:
    """
    Retrieves the trending tracks for a specific genre from Deezer.

    :param limit: Number of tracks to retrieve (default is 50).
    :param index: Starting point for the tracks (default is 0).
    :return: A list of dictionaries containing track information (title, artist, and URL).
    """
    genre_id: int = get_genre_id()

    # Deezer Charts API URL with the genre ID
    url: str = f"https://api.deezer.com/chart/{genre_id}?limit={limit}&index={index}"
    response = requests.get(url)
    chart_data: Dict[str, Any] = response.json()

    trending_tracks: List[Dict[str, str]] = []

    # Extract titles and Deezer URLs
    for track in chart_data["tracks"]["data"]:
        title: str = track["title"]
        artist: str = track["artist"]["name"]
        track_url: str = track["link"]
        trending_tracks.append({"title": title, "artist": artist, "url": track_url})

    return trending_tracks


def download_with_ytdlp(
    deezer_url: str, codec: str = "mp3", quality: str = "bestaudio"
):
    """
    Uses yt-dlp to download a Deezer track and convert it to the specified codec and quality.

    :param deezer_url: Deezer URL of the track or album.
    :param codec: Desired audio format (default is mp3).
    :param quality: Audio quality (default is bestaudio).
    """
    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format",
        codec,
        "--audio-quality",
        quality,
        "--output",
        f"{DESTINATION_FOLDER}/%(title)s.%(ext)s",
        deezer_url,
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Successfully downloaded and converted {deezer_url}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download {deezer_url}: {e}")


if __name__ == "__main__":
    # Get trending tracks based on today's genre
    trending_tracks: List[Dict[str, Any]] = get_deezer_genre_tracks()

    # Load download history
    download_history = load_download_history()

    # Filter out already downloaded tracks and only take the first 10
    new_tracks = filter_new_tracks(trending_tracks, download_history, limit=10)
    
    # Save the download history
    save_download_history(new_tracks)

    # Get the youtube urls for the trending tracks
    youtube_urls = []
    for track in new_tracks:
        try:
            video = json.loads(
                YoutubeSearch(
                    track["title"] + " " + track["artist"], max_results=1
                ).to_json()
            )

            url = (
                "https://www.youtube.com/"
                + video.get("videos")[0].get("url_suffix")
            )
        except Exception as e:
            print(f"Failed to get youtube url for {track['title']} by {track['artist']} - {e}")
            continue
        youtube_urls.append({"title": track["title"], "artist": track["artist"], "url": url})

    # Download each track using yt-dlp
    for track in youtube_urls:
        yt_url = track["url"]
        print(f"Downloading track: {track['title']} by {track['artist']}")
        download_with_ytdlp(yt_url)
