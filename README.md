# 🎮 Gaming Reel Maker

An automated AI-powered pipeline that generates gaming lore/storyline breakdown videos and posts them as **Instagram Reels** and **YouTube Shorts** — daily, hands-free.

## 🎯 Games Covered
- GTA V / GTA VI
- Valorant
- Call of Duty
- Fortnite
- Roblox

## 🔄 Pipeline

```
Script (Gemini AI) → Voiceover (ElevenLabs) → Stock Clips (Pexels) → 9:16 Video (FFmpeg) → Post (Instagram + YouTube)
```

## 🚀 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

> You'll also need **FFmpeg** installed on your system:
> - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
> - Mac: `brew install ffmpeg`

### 2. Configure API keys
```bash
cp .env.example .env
# Edit .env and fill in your keys
```

**APIs you need:**
| Service | Purpose | Free Tier |
|---|---|---|
| [Google AI Studio](https://aistudio.google.com) | Script generation | ✅ Yes |
| [ElevenLabs](https://elevenlabs.io) | AI voiceover | ✅ Yes (10k chars/mo) |
| [Pexels](https://www.pexels.com/api/) | Stock footage | ✅ Yes (unlimited) |
| [Meta for Developers](https://developers.facebook.com) | Instagram posting | ✅ Yes |
| [Google Cloud Console](https://console.cloud.google.com) | YouTube posting | ✅ Yes |

### 3. Run once (test)
```bash
# Random game
python main.py

# Specific game
python main.py --game "GTA V"
```

### 4. Run on daily schedule (6 PM IST)
```bash
python main.py --schedule
```

## 📁 Project Structure

```
gaming-reel-maker/
├── main.py               # Orchestrator + scheduler
├── config.py             # Settings & API keys loader
├── script_generator.py   # Gemini AI script writer
├── voiceover.py          # ElevenLabs TTS
├── video_fetcher.py      # Pexels stock clip downloader
├── video_assembler.py    # FFmpeg/MoviePy video composer
├── publisher.py          # Instagram + YouTube uploader
├── requirements.txt
├── .env.example          # Template for your keys
├── .gitignore
└── output/               # Final rendered videos (gitignored)
```

## ⚠️ Notes

- `output/` and `temp/` folders are **gitignored** — videos stay local
- Never commit your `.env` file
- Instagram requires videos to be hosted at a **public URL** before posting — consider Cloudinary (free tier) for hosting

## 📄 License
MIT
