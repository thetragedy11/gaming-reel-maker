"""
video_fetcher.py
Fetches relevant stock video clips from Pexels API based on game name.
"""

import os
import requests
import random
from config import PEXELS_API_KEY, TEMP_DIR


GAME_SEARCH_TERMS = {
    "GTA V":        ["los angeles city night", "heist crime", "luxury car chase", "city skyline"],
    "GTA VI":       ["miami beach night", "neon city", "crime thriller", "open world"],
    "Valorant":     ["futuristic combat", "tactical shooter", "neon lights action", "cyberpunk city"],
    "Call of Duty": ["military action", "war zone", "soldier combat", "battlefield explosion"],
    "Fortnite":     ["battle royale", "storm lightning", "island survival", "colorful action"],
    "Roblox":       ["virtual world", "blocky adventure", "creative gaming", "colorful digital"],
}

DEFAULT_TERMS = ["gaming setup", "gaming neon lights", "controller gaming", "esports arena"]


def fetch_video_clips(game: str, num_clips: int = 4) -> list:
    """
    Fetch relevant video clip URLs from Pexels for the given game.

    Returns:
        List of local file paths for downloaded clips
    """
    os.makedirs(TEMP_DIR, exist_ok=True)

    search_terms = GAME_SEARCH_TERMS.get(game, DEFAULT_TERMS)
    query = random.choice(search_terms)

    print(f"[VideoFetcher] Searching Pexels for: '{query}'")

    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "per_page": 15,
        "orientation": "portrait",   # vertical for reels
        "size": "medium",
    }

    resp = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
    if resp.status_code != 200:
        raise Exception(f"Pexels error {resp.status_code}: {resp.text}")

    videos = resp.json().get("videos", [])
    if not videos:
        raise Exception(f"No Pexels videos found for query: {query}")

    # Pick random clips, prefer HD
    selected = random.sample(videos, min(num_clips, len(videos)))
    clip_paths = []

    for i, video in enumerate(selected):
        # Get the best quality video file (HD preferred)
        video_files = sorted(
            video["video_files"],
            key=lambda x: x.get("width", 0),
            reverse=True,
        )
        video_url = video_files[0]["link"]

        clip_path = os.path.join(TEMP_DIR, f"clip_{i}.mp4")
        print(f"[VideoFetcher] Downloading clip {i+1}/{num_clips}...")

        clip_resp = requests.get(video_url, stream=True)
        with open(clip_path, "wb") as f:
            for chunk in clip_resp.iter_content(chunk_size=8192):
                f.write(chunk)

        clip_paths.append(clip_path)
        print(f"[VideoFetcher] Saved: {clip_path}")

    return clip_paths


if __name__ == "__main__":
    clips = fetch_video_clips("GTA V", num_clips=2)
    print(f"Downloaded clips: {clips}")
