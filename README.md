gTTS – Simple Desktop Text To Speech App

A simple desktop application that uses gTTS (Google Text-to-Speech – free) to convert text into MP3 audio files.
Suitable for personal use, demos, and learning purposes.

⚠️ Limit: ~60,000 characters per hour (Google policy, IP-based limit).

📦 Project Structure
gTTS/
├── merge.py              # Audio generator app (NO FFmpeg required)
├── only_gtts.py          # Audio + video merge app (FFmpeg REQUIRED)
├── requirements.txt
└── README.md

1️⃣ tts_app.py – Generate MP3 Audio (NO FFmpeg Required)
✔ Features

Convert text input into multiple .mp3 files

Automatically split long text to avoid gTTS errors

Track usage limit (60,000 characters per hour)

Support multiple languages (default: Vietnamese)

Desktop UI built with PyQt6

No pydub used → FFmpeg is NOT required

✔ Required Libraries
pip install gtts PyQt6

▶ Run the app
python tts_app.py

📁 Output

Generated MP3 files will be saved in:

AmThanh_Output/

2️⃣ video_audio_merger.py – Merge Audio into Video (FFmpeg REQUIRED)

⚠️ This file does NOT use gTTS
👉 It is only used to merge existing .mp3 audio into multiple .mp4 videos.

✔ Features

Select multiple video files (.mp4)

Select one audio file (.mp3)

Automatically trim audio or video to match duration

Export merged videos as _merged.mp4

Lightweight UI built with Tkinter

❗ Requirements

FFmpeg

moviepy

🔧 Install FFmpeg (Windows)

Download FFmpeg:
👉 https://ffmpeg.org/download.html

Extract the archive

Add the bin folder to PATH

Verify installation:

ffmpeg -version