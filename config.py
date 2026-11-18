# ============================================================
# config.py — Central configuration for Gaming Reel Maker
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
GEMINI_API_KEY        = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY    = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID   = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
PEXELS_API_KEY        = os.getenv("PEXELS_API_KEY")

INSTAGRAM_ACCESS_TOKEN       = os.getenv("INSTAGRAM_ACCESS_TOKEN")
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")

YOUTUBE_CLIENT_ID     = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")

# --- Game Library ---
GAMES = [
    "GTA V",
    "GTA VI",
    "Valorant",
    "Call of Duty",
    "Fortnite",
    "Roblox",
]

# --- Content Settings ---
CONTENT_TYPE = "lore and storyline breakdown"
VIDEO_DURATION_SECONDS = 55       # Target ~55s (safe for Reels & Shorts)
SCRIPT_WORD_COUNT = 130           # ~130 words ≈ 55s at avg speaking pace

# --- Video Settings ---
VIDEO_WIDTH  = 1080
VIDEO_HEIGHT = 1920               # 9:16 vertical
VIDEO_FPS    = 30
FONT_SIZE    = 52
SUBTITLE_COLOR = "white"
SUBTITLE_STROKE_COLOR = "black"
SUBTITLE_STROKE_WIDTH = 2

# --- Output Paths ---
OUTPUT_DIR = "output"
TEMP_DIR   = "temp"

# --- Scheduler ---
POST_HOUR   = 18   # 6 PM IST daily
POST_MINUTE = 0
