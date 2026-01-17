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

1️⃣ only_gtts.py – Generate MP3 Audio (NO FFmpeg Required)
✔ Features

Convert text input into multiple .mp3 files

Automatically split long text to avoid gTTS errors

Track usage limit (60,000 characters per hour)

Support multiple languages (default: Vietnamese)

Desktop UI built with PyQt6

No pydub used → FFmpeg is NOT required

✔ Required Libraries
pip install gtts PyQt6
pip install -r requirements.txt

▶ Run the app
python only_gtts.py

📁 Output

Generated MP3 files will be saved in:

AmThanh_Output/

2️⃣ merge.py – Merge Audio into Video (FFmpeg REQUIRED)

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

-- Build file to app .exe
1️⃣ Install PyInstaller
pip install pyinstaller

2️⃣ Build the TTS app (only_gtts.py)

This app does NOT require FFmpeg and is recommended for .exe distribution.

pyinstaller --onefile --windowed only_gtts.py

Flags explained:

--onefile → bundle everything into a single .exe

--windowed → hide the console window (GUI app)

3️⃣ Output location

After the build completes, the executable will be located at:

dist/only_gtts.exe


You only need to distribute the file inside the dist folder.

4️⃣ Run the executable

Double-click only_gtts.exe

Enter text

Click Download MP3

Output files will be saved to:

AmThanh_Output/