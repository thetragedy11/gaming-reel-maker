"""
publisher.py
Posts the final reel to Instagram Reels and YouTube Shorts.
"""

import os
import time
import requests
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from config import (
    INSTAGRAM_ACCESS_TOKEN,
    INSTAGRAM_BUSINESS_ACCOUNT_ID,
    YOUTUBE_CLIENT_ID,
    YOUTUBE_CLIENT_SECRET,
    YOUTUBE_REFRESH_TOKEN,
)


# ─────────────────────────────────────────────
# INSTAGRAM
# ─────────────────────────────────────────────

def publish_to_instagram(video_path: str, caption: str, hashtags: str) -> bool:
    """
    Upload a reel to Instagram using the Graph API.
    NOTE: Instagram requires the video to be hosted at a public URL.
    You'll need to upload to a CDN (e.g. Cloudinary, S3) first, or use
    a container upload approach.
    """
    full_caption = f"{caption}\n\n{hashtags}"

    # Step 1: Create media container
    container_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
    container_payload = {
        "media_type": "REELS",
        "video_url": video_path,     # Must be a public HTTPS URL
        "caption": full_caption,
        "share_to_feed": True,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }

    print("[Instagram] Creating media container...")
    resp = requests.post(container_url, data=container_payload)
    data = resp.json()

    if "id" not in data:
        print(f"[Instagram] Container error: {data}")
        return False

    container_id = data["id"]
    print(f"[Instagram] Container ID: {container_id}")

    # Step 2: Wait for video processing
    print("[Instagram] Waiting for video processing (30s)...")
    time.sleep(30)

    # Step 3: Check status
    status_url = f"https://graph.facebook.com/v19.0/{container_id}?fields=status_code&access_token={INSTAGRAM_ACCESS_TOKEN}"
    for attempt in range(5):
        status_resp = requests.get(status_url).json()
        status = status_resp.get("status_code", "")
        print(f"[Instagram] Status: {status}")
        if status == "FINISHED":
            break
        time.sleep(15)

    # Step 4: Publish
    publish_url = f"https://graph.facebook.com/v19.0/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
    publish_payload = {
        "creation_id": container_id,
        "access_token": INSTAGRAM_ACCESS_TOKEN,
    }

    pub_resp = requests.post(publish_url, data=publish_payload).json()
    if "id" in pub_resp:
        print(f"[Instagram] ✅ Published! Post ID: {pub_resp['id']}")
        return True
    else:
        print(f"[Instagram] Publish error: {pub_resp}")
        return False


# ─────────────────────────────────────────────
# YOUTUBE
# ─────────────────────────────────────────────

def get_youtube_service():
    """Authenticate and return YouTube API service."""
    creds = Credentials(
        token=None,
        refresh_token=YOUTUBE_REFRESH_TOKEN,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=YOUTUBE_CLIENT_ID,
        client_secret=YOUTUBE_CLIENT_SECRET,
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    # Refresh token to get valid access token
    request = google.auth.transport.requests.Request()
    creds.refresh(request)
    return build("youtube", "v3", credentials=creds)


def publish_to_youtube(video_path: str, title: str, description: str, hashtags: str) -> bool:
    """Upload a Short to YouTube."""
    print("[YouTube] Authenticating...")
    youtube = get_youtube_service()

    full_description = f"{description}\n\n{hashtags}\n\n#Shorts"
    tags = [tag.replace("#", "") for tag in hashtags.split()]

    body = {
        "snippet": {
            "title": f"{title} #Shorts",
            "description": full_description,
            "tags": tags + ["Shorts", "Gaming", "GamingLore"],
            "categoryId": "20",    # Gaming category
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")

    print("[YouTube] Uploading Short...")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            progress = int(status.progress() * 100)
            print(f"[YouTube] Upload progress: {progress}%")

    video_id = response.get("id")
    if video_id:
        print(f"[YouTube] ✅ Published! https://youtube.com/shorts/{video_id}")
        return True
    else:
        print(f"[YouTube] Upload error: {response}")
        return False


# ─────────────────────────────────────────────
# COMBINED PUBLISHER
# ─────────────────────────────────────────────

def publish_reel(video_path: str, title: str, script: str, hashtags: str):
    """Publish to both Instagram and YouTube."""
    print("\n📤 Publishing to platforms...")

    ig_success = publish_to_instagram(video_path, f"🎮 {title}", hashtags)
    yt_success = publish_to_youtube(video_path, title, script[:200], hashtags)

    if ig_success and yt_success:
        print("\n✅ Successfully posted to Instagram Reels + YouTube Shorts!")
    elif ig_success:
        print("\n⚠️  Posted to Instagram only.")
    elif yt_success:
        print("\n⚠️  Posted to YouTube only.")
    else:
        print("\n❌ Publishing failed on both platforms. Check your API keys.")

    return ig_success, yt_success
