import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip, AudioFileClip  # pyright: ignore[reportMissingImports]

import os

class VideoAudioMergerApp:
    def __init__(self, root):
        self.root = root
        root.title("Batch Ghép Audio vào Video")

        self.video_paths = []
        self.audio_path = ""

        # Video Listbox
        tk.Label(root, text="Video (.mp4) list:").pack()
        self.listbox = tk.Listbox(root, width=60, height=10)
        self.listbox.pack(pady=5)

        # Buttons chọn file
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Thêm video", command=self.add_videos).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa video đã chọn", command=self.remove_selected).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Chọn audio (.mp3)", command=self.select_audio).pack(side=tk.LEFT, padx=5)

        # Audio file label
        self.audio_label = tk.Label(root, text="Chưa chọn audio")
        self.audio_label.pack(pady=5)

        # Merge button
        tk.Button(root, text="Ghép tất cả & Xuất", command=self.batch_merge, bg="green", fg="white").pack(pady=10)

    def add_videos(self):
        files = filedialog.askopenfilenames(filetypes=[("MP4 files", "*.mp4")])
        for f in files:
            if f not in self.video_paths:
                self.video_paths.append(f)
                self.listbox.insert(tk.END, f)

    def remove_selected(self):
        selected = self.listbox.curselection()
        for i in reversed(selected):
            self.listbox.delete(i)
            self.video_paths.pop(i)

    def select_audio(self):
        path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if path:
            self.audio_path = path
            self.audio_label.config(text=os.path.basename(path))

    def batch_merge(self):
        if not self.video_paths:
            messagebox.showerror("Lỗi", "Bạn chưa thêm video nào.")
            return
        if not self.audio_path:
            messagebox.showerror("Lỗi", "Bạn chưa chọn file âm thanh.")
            return

        try:
            audio_full = AudioFileClip(self.audio_path)
            output_dir = filedialog.askdirectory(title="Chọn thư mục lưu video xuất")
            if not output_dir:
                return

            for video_path in self.video_paths:
                video = VideoFileClip(video_path)

                # So sánh thời lượng video và audio để cắt đúng
                if video.duration > audio_full.duration:
                    video_cut = video.subclip(0, audio_full.duration)
                    audio_cut = audio_full
                else:
                    video_cut = video
                    audio_cut = audio_full.subclip(0, video.duration)

                video_cut = video_cut.set_audio(audio_cut)

                base_name = os.path.splitext(os.path.basename(video_path))[0]
                output_path = os.path.join(output_dir, f"{base_name}_merged.mp4")

                video_cut.write_videofile(output_path, fps=24)

            messagebox.showinfo("Hoàn thành", "Đã ghép xong tất cả video!")

        except Exception as e:
            messagebox.showerror("Lỗi", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoAudioMergerApp(root)
    root.mainloop()
