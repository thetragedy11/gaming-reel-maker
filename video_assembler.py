"""
video_assembler.py
Assembles stock clips + voiceover + subtitles into a final 9:16 reel.
Uses MoviePy + FFmpeg.
"""

import os
import textwrap
from moviepy.editor import (
    VideoFileClip, AudioFileClip, concatenate_videoclips,
    TextClip, CompositeVideoClip, ColorClip
)
from config import (
    VIDEO_WIDTH, VIDEO_HEIGHT, VIDEO_FPS,
    FONT_SIZE, SUBTITLE_COLOR, SUBTITLE_STROKE_COLOR, SUBTITLE_STROKE_WIDTH,
    OUTPUT_DIR, TEMP_DIR
)


def crop_to_vertical(clip):
    """Crop a clip to 9:16 aspect ratio centered."""
    target_ratio = VIDEO_WIDTH / VIDEO_HEIGHT
    clip_ratio = clip.w / clip.h

    if clip_ratio > target_ratio:
        # Clip is wider than needed — crop sides
        new_width = int(clip.h * target_ratio)
        x_center = clip.w // 2
        clip = clip.crop(x1=x_center - new_width // 2, x2=x_center + new_width // 2)
    else:
        # Clip is taller — crop top/bottom
        new_height = int(clip.w / target_ratio)
        y_center = clip.h // 2
        clip = clip.crop(y1=y_center - new_height // 2, y2=y_center + new_height // 2)

    return clip.resize((VIDEO_WIDTH, VIDEO_HEIGHT))


def create_subtitle_clips(script: str, audio_duration: float):
    """Split script into timed subtitle chunks."""
    words = script.split()
    words_per_second = len(words) / audio_duration
    chunk_size = max(4, int(words_per_second * 2.5))  # ~2.5s per subtitle

    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    subtitle_clips = []
    duration_per_chunk = audio_duration / len(chunks)

    for i, chunk in enumerate(chunks):
        txt = TextClip(
            textwrap.fill(chunk, width=28),
            fontsize=FONT_SIZE,
            color=SUBTITLE_COLOR,
            stroke_color=SUBTITLE_STROKE_COLOR,
            stroke_width=SUBTITLE_STROKE_WIDTH,
            font="Arial-Bold",
            method="caption",
            size=(VIDEO_WIDTH - 80, None),
            align="center",
        )
        txt = txt.set_start(i * duration_per_chunk)
        txt = txt.set_duration(duration_per_chunk)
        txt = txt.set_position(("center", VIDEO_HEIGHT - 350))
        subtitle_clips.append(txt)

    return subtitle_clips


def assemble_video(clip_paths: list, voiceover_path: str, script: str, output_filename: str = "reel.mp4") -> str:
    """
    Combine video clips + voiceover + subtitles into final reel.

    Returns:
        Path to the final rendered MP4
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    print("[Assembler] Loading audio...")
    audio = AudioFileClip(voiceover_path)
    total_duration = audio.duration

    print("[Assembler] Processing video clips...")
    processed_clips = []
    per_clip_duration = total_duration / len(clip_paths)

    for path in clip_paths:
        clip = VideoFileClip(path)
        clip = crop_to_vertical(clip)

        # Loop or trim clip to match needed duration
        if clip.duration < per_clip_duration:
            loops = int(per_clip_duration / clip.duration) + 1
            clip = concatenate_videoclips([clip] * loops)
        clip = clip.subclip(0, per_clip_duration)
        processed_clips.append(clip)

    print("[Assembler] Concatenating clips...")
    base_video = concatenate_videoclips(processed_clips, method="compose")
    base_video = base_video.subclip(0, total_duration)

    print("[Assembler] Generating subtitles...")
    subtitle_clips = create_subtitle_clips(script, total_duration)

    print("[Assembler] Compositing final video...")
    final = CompositeVideoClip([base_video] + subtitle_clips)
    final = final.set_audio(audio)
    final = final.set_duration(total_duration)

    print(f"[Assembler] Rendering to: {output_path}")
    final.write_videofile(
        output_path,
        fps=VIDEO_FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast",
        verbose=False,
        logger=None,
    )

    # Cleanup temp files
    for path in clip_paths:
        try:
            os.remove(path)
        except Exception:
            pass
    try:
        os.remove(voiceover_path)
    except Exception:
        pass

    print(f"[Assembler] Done! Final video: {output_path}")
    return output_path


if __name__ == "__main__":
    print("Run main.py to test the full pipeline.")
