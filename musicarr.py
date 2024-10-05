import json
import requests
import datetime
import subprocess
from typing import List, Dict, Any
from youtube_search import YoutubeSearch
import sys

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


def get_deezer_genre_tracks(limit: int = 10, index: int = 0) -> List[Dict[str, Any]]:
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

    # Get the youtube urls for the trending tracks
    youtube_urls = []
    for track in trending_tracks:
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
