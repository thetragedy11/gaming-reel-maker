"""
voiceover.py
Converts a text script to an MP3 voiceover using ElevenLabs TTS.
"""

import os
import requests
from config import ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID, TEMP_DIR


def generate_voiceover(script: str, output_filename: str = "voiceover.mp3") -> str:
    """
    Send script to ElevenLabs and save the MP3 voiceover.

    Args:
        script: The spoken text
        output_filename: Filename for the output MP3

    Returns:
        Path to the saved MP3 file
    """
    os.makedirs(TEMP_DIR, exist_ok=True)
    output_path = os.path.join(TEMP_DIR, output_filename)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.3,
            "use_speaker_boost": True,
        },
    }

    print(f"[Voiceover] Requesting ElevenLabs TTS...")
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        raise Exception(f"ElevenLabs error {response.status_code}: {response.text}")

    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"[Voiceover] Saved to: {output_path}")
    return output_path


if __name__ == "__main__":
    test_script = "In the world of GTA V, three criminals unite for the greatest heist Los Santos has ever seen."
    path = generate_voiceover(test_script, "test_voice.mp3")
    print(f"Voiceover saved: {path}")
