"""Podcast processing pipeline.

This module provides a CLI tool capable of downloading an audio file from a
streaming URL, transcribing the spoken content, translating the transcript to
Greek, and synthesising the translation back into speech.

The default implementation relies on external services (Google Translate via
``googletrans`` and Google Text-to-Speech via ``gTTS``) and therefore requires
an active internet connection. It also uses ``yt-dlp`` to retrieve the audio and
``whisper`` to perform transcription.
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional

from googletrans import Translator
from gtts import gTTS
from yt_dlp import YoutubeDL

try:
    import whisper
except ImportError as exc:  # pragma: no cover - surface friendly message
    raise SystemExit(
        "The 'whisper' package is required. Install dependencies with "
        "`pip install -r requirements.txt`."
    ) from exc

LOGGER = logging.getLogger(__name__)


def download_audio(url: str, output_dir: Path) -> Path:
    """Download ``url`` and return the path to the extracted audio file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(str(output_dir), "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    LOGGER.info("Downloading audio from %s", url)
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded = ydl.prepare_filename(info)
    except Exception as exc:  # pragma: no cover - network/DRM errors
        raise RuntimeError(
            "Failed to download audio. Many platforms (including Spotify) "
            "protect their streams with DRM, which prevents automated "
            "downloads."
        ) from exc

    mp3_path = Path(os.path.splitext(downloaded)[0] + ".mp3")
    if not mp3_path.exists():
        raise FileNotFoundError(
            "The audio file was not created as expected. Ensure ffmpeg is "
            "installed."
        )

    LOGGER.debug("Downloaded audio saved to %s", mp3_path)
    return mp3_path


def transcribe_audio(audio_path: Path, model_name: str = "base") -> tuple[str, str]:
    """Transcribe ``audio_path`` using Whisper ``model_name``."""
    LOGGER.info("Loading Whisper model '%s'", model_name)
    model = whisper.load_model(model_name)
    LOGGER.info("Transcribing audio %s", audio_path)
    result = model.transcribe(str(audio_path))
    transcript = result.get("text", "").strip()
    language = result.get("language", "unknown")
    if not transcript:
        raise RuntimeError("Transcription produced no text.")

    LOGGER.debug("Detected language: %s", language)
    return transcript, language


def translate_text(text: str, target_language: str = "el") -> str:
    """Translate ``text`` into ``target_language`` using Google Translate."""
    LOGGER.info("Translating transcript to %s", target_language)
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    translated_text = translation.text.strip()
    if not translated_text:
        raise RuntimeError("Translation produced no text.")
    return translated_text


def synthesise_speech(text: str, output_path: Path, language: str = "el") -> Path:
    """Convert ``text`` to speech and save it to ``output_path``."""
    LOGGER.info("Synthesising translated text to speech (%s)", language)
    tts = gTTS(text=text, lang=language)
    tts.save(str(output_path))
    LOGGER.debug("Synthesised audio saved to %s", output_path)
    return output_path


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Transcribe and translate podcasts")
    parser.add_argument("url", help="Streaming URL (podcast episode, audio file, etc.)")
    parser.add_argument(
        "--model",
        default="base",
        help="Whisper model name to use (tiny, base, small, medium, large).",
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="Directory where transcripts and audio will be stored.",
    )
    parser.add_argument(
        "--target-language",
        default="el",
        help="BCP-47 language code for translation and speech synthesis.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging verbosity (DEBUG, INFO, WARNING, ERROR).",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO))

    output_dir = Path(args.output_dir)
    try:
        audio_path = download_audio(args.url, output_dir)
        transcript, detected_language = transcribe_audio(audio_path, args.model)
        translated_text = translate_text(transcript, target_language=args.target_language)

        transcript_path = output_dir / "transcript.txt"
        transcript_path.write_text(transcript, encoding="utf-8")
        LOGGER.info("Transcript saved to %s", transcript_path)

        translation_path = output_dir / f"translation_{args.target_language}.txt"
        translation_path.write_text(translated_text, encoding="utf-8")
        LOGGER.info("Translation saved to %s", translation_path)

        speech_path = output_dir / f"translation_{args.target_language}.mp3"
        synthesise_speech(translated_text, speech_path, language=args.target_language)
        LOGGER.info("Spoken translation saved to %s", speech_path)

        LOGGER.info("Detected source language: %s", detected_language)
    except Exception as exc:  # pragma: no cover - CLI entry point
        LOGGER.error("Processing failed: %s", exc)
        return 1

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI usage
    sys.exit(main())
