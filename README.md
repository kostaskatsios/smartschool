# smartschool Podcast Translator

This repository now contains a simple command-line utility that can download a
podcast episode, generate a transcription, translate the transcript into
another language (Greek by default) and finally produce an audio rendering of
the translated text.

> ⚠️ **Important limitation:** Many commercial streaming platforms – including
> Spotify – protect their audio streams with DRM. The downloader used by this
> tool (``yt-dlp``) cannot bypass DRM. For such platforms you will need to obtain
> the audio file via an alternative, legally compliant source before using the
> tool.

## Requirements

* Python 3.9+
* `ffmpeg` installed and available on your `PATH`
* Network connectivity for Google Translate and Google Text-to-Speech
* Python dependencies listed in `requirements.txt`

Install the dependencies with:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python podcast_processor.py "<audio or podcast URL>"
```

Optional arguments:

* `--model`: Whisper model name (default: `base`).
* `--output-dir`: directory where the transcript, translation and audio files
  will be stored (default: `outputs`).
* `--target-language`: BCP-47 code for the translation and speech synthesis
  (default: `el` for Greek).
* `--log-level`: logging verbosity (default: `INFO`).

The tool produces three files inside the output directory:

1. `transcript.txt` – transcription of the original language.
2. `translation_<lang>.txt` – translated text.
3. `translation_<lang>.mp3` – the translation read aloud.

## Example

```bash
python podcast_processor.py "https://example.com/audio.mp3" \
  --target-language el --output-dir podcast_output
```

This command downloads the audio, generates a transcript, translates it into
Greek and creates an MP3 file with the translated narration.
