"""
main.py — Gaming Reel Maker
Orchestrates the full pipeline: Script → Voice → Video → Post
Run once manually, or let the scheduler run it daily.
"""

import os
import time
import schedule
import datetime
from config import GAMES, POST_HOUR, POST_MINUTE, TEMP_DIR, OUTPUT_DIR
from script_generator import generate_script
from voiceover import generate_voiceover
from video_fetcher import fetch_video_clips
from video_assembler import assemble_video
from publisher import publish_reel


def run_pipeline(game: str = None):
    """Full pipeline: generate → assemble → publish one reel."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\n{'='*55}")
    print(f"  🎮 Gaming Reel Maker — {timestamp}")
    print(f"{'='*55}\n")

    os.makedirs(TEMP_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: Generate script
    print("📝 Step 1/4: Generating script...")
    content = generate_script(game)
    game_name = content["game"]
    script    = content["script"]
    title     = content["title"]
    hashtags  = content["hashtags"]

    # Step 2: Generate voiceover
    print("\n🎙️  Step 2/4: Generating voiceover...")
    voice_path = generate_voiceover(script, f"voice_{timestamp}.mp3")

    # Step 3: Fetch and assemble video
    print("\n🎬 Step 3/4: Fetching clips & assembling video...")
    clip_paths = fetch_video_clips(game_name, num_clips=4)
    video_path = assemble_video(
        clip_paths,
        voice_path,
        script,
        output_filename=f"reel_{timestamp}.mp4"
    )

    # Step 4: Publish
    print("\n📤 Step 4/4: Publishing...")
    publish_reel(video_path, title, script, hashtags)

    print(f"\n✅ Pipeline complete! Game: {game_name}")
    print(f"   Video saved at: {video_path}\n")


def run_scheduler():
    """Run the pipeline daily at the configured time (IST)."""
    post_time = f"{POST_HOUR:02d}:{POST_MINUTE:02d}"
    print(f"⏰ Scheduler active — posting daily at {post_time} IST")
    print("   Press Ctrl+C to stop.\n")

    schedule.every().day.at(post_time).do(run_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Gaming Reel Maker")
    parser.add_argument(
        "--game",
        type=str,
        default=None,
        help=f"Game to make reel for. Options: {', '.join(GAMES)}. Leave blank for random.",
    )
    parser.add_argument(
        "--schedule",
        action="store_true",
        help="Run on daily schedule instead of once",
    )
    args = parser.parse_args()

    if args.schedule:
        run_scheduler()
    else:
        run_pipeline(game=args.game)
