gTTS – Simple Desktop Text To Speech App

Ứng dụng desktop đơn giản sử dụng gTTS (Google Text-to-Speech miễn phí) để chuyển văn bản thành file MP3.
Phù hợp cho nhu cầu cá nhân, demo, học tập.

⚠️ Giới hạn: ~60.000 ký tự / giờ (theo chính sách Google, giới hạn theo IP).

📦 Cấu trúc project
gTTS/
├── merge.py              # App tạo audio MP3 (KHÔNG cần FFmpeg)
├── only_gtts.py   # App ghép audio vào video (CẦN FFmpeg)
├── requirements.txt
└── README.md

1️⃣ File only_gtts.py – Tạo Audio MP3 (KHÔNG cần FFmpeg)
✔ Chức năng

Nhập văn bản → xuất nhiều file .mp3

Tự chia nhỏ text để tránh lỗi gTTS

Theo dõi hạn mức 60.000 ký tự / giờ

Hỗ trợ nhiều ngôn ngữ (mặc định Tiếng Việt)

Giao diện PyQt6

Không dùng pydub → không cần FFmpeg

✔ Thư viện sử dụng
pip install gtts PyQt6
pip install -r requirements.txt

✔ Chạy chương trình
python only_gtts.py

📁 Output

File MP3 được lưu trong thư mục:

AmThanh_Output/

2️⃣ File merge.py – Ghép Audio vào Video (BẮT BUỘC FFmpeg)

⚠️ File này KHÔNG dùng gTTS
👉 Chỉ dùng để ghép file MP3 có sẵn vào nhiều video MP4

✔ Chức năng

Chọn nhiều video (.mp4)

Chọn 1 audio (.mp3)

Tự cắt audio / video cho khớp thời lượng

Xuất video mới _merged.mp4

Giao diện Tkinter (nhẹ, đơn giản)

❗ Yêu cầu bắt buộc

FFmpeg

moviepy

🔧 Cài FFmpeg
Windows

Tải FFmpeg:
👉 https://ffmpeg.org/download.html

Giải nén

Thêm thư mục bin vào PATH

Kiểm tra:

ffmpeg -version

🧊 Build file thành ứng dụng .exe
1️⃣ Cài PyInstaller
pip install pyinstaller

2️⃣ Build ứng dụng TTS (only_gtts.py)

Ứng dụng này KHÔNG cần FFmpeg và được khuyến nghị để build ra file .exe.

pyinstaller --onefile --windowed only_gtts.py

Giải thích các tham số:

--onefile → gộp toàn bộ thành một file .exe duy nhất

--windowed → ẩn cửa sổ console (dành cho ứng dụng giao diện)

3️⃣ Vị trí file output

Sau khi build xong, file .exe sẽ nằm tại:

dist/only_gtts.exe


👉 Bạn chỉ cần phân phối file trong thư mục dist.

4️⃣ Chạy ứng dụng

Double-click only_gtts.exe

Nhập nội dung văn bản

Bấm Download MP3

File âm thanh sẽ được lưu tại:

AmThanh_Output/