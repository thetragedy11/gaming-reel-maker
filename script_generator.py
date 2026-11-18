"""
script_generator.py
Generates a ~55-second gaming lore/storyline breakdown script
using Google Gemini (or OpenAI as fallback).
"""

import random
import google.generativeai as genai
from config import GEMINI_API_KEY, GAMES, CONTENT_TYPE, SCRIPT_WORD_COUNT


def generate_script(game: str = None) -> dict:
    """
    Generate a voiceover script for a gaming reel.

    Returns:
        dict with keys: game, title, script, hashtags
    """
    if game is None:
        game = random.choice(GAMES)

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"""
You are a viral gaming content creator on YouTube Shorts and Instagram Reels.
Write a {SCRIPT_WORD_COUNT}-word voiceover script for a {CONTENT_TYPE} about "{game}".

Rules:
- Hook the viewer in the FIRST sentence (make it shocking or intriguing)
- Keep sentences short and punchy — this is spoken content
- Build suspense, reveal lore facts, end with a cliffhanger or mic-drop moment
- Do NOT use markdown formatting, bullet points, or headers — plain text only
- Write exactly as it should be spoken aloud

Also provide:
- A catchy reel TITLE (max 10 words)
- 10 relevant Instagram/YouTube hashtags

Format your response EXACTLY like this:
TITLE: <title here>
SCRIPT: <script here>
HASHTAGS: <hashtags here>
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    # Parse response
    title, script, hashtags = "", "", ""
    for line in text.split("\n"):
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("SCRIPT:"):
            script = line.replace("SCRIPT:", "").strip()
        elif line.startswith("HASHTAGS:"):
            hashtags = line.replace("HASHTAGS:", "").strip()

    # Fallback: if multi-line script
    if not script:
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("SCRIPT:"):
                script = " ".join(lines[i:]).replace("SCRIPT:", "").replace("HASHTAGS:", "").strip()
                break

    print(f"[ScriptGen] Game: {game}")
    print(f"[ScriptGen] Title: {title}")
    print(f"[ScriptGen] Script preview: {script[:80]}...")

    return {
        "game": game,
        "title": title,
        "script": script,
        "hashtags": hashtags,
    }


if __name__ == "__main__":
    result = generate_script("GTA V")
    print("\n--- Generated Script ---")
    print(f"Title: {result['title']}")
    print(f"Script: {result['script']}")
    print(f"Hashtags: {result['hashtags']}")
