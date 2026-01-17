import sys
import os
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QFileDialog
from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSignal, QObject
from gtts import gTTS, lang

# Loại bỏ pydub để giảm dung lượng và tránh lỗi FFmpeg
# from pydub import AudioSegment 

BASE_FILE_NAME_DETAIL = "output_part_"
CHAR_LIMIT_PER_HOUR = 60000 

def extract_number(filename):
    try:
        replace = filename.replace(".mp3", "").replace(BASE_FILE_NAME_DETAIL, "")
        return int(replace)
    except:
        return 0

def format_textinput(input_str: str) -> str:
    input_str = re.sub(r'[?!]', '.', input_str)
    input_str = re.sub(r'\n', '. ', input_str)
    input_str = re.sub(r'"', ' ', input_str)
    input_str = re.sub(r'\s+', ' ', input_str)
    input_str = re.sub(r'\.{2,}', '.', input_str)
    return input_str.strip()

class WorkerSignals(QObject):
    finished = pyqtSignal(list)
    progress = pyqtSignal(int, int)
    error_429 = pyqtSignal()

class GTTSWorker(QRunnable):
    def __init__(self, parts, lang, slow, folder_path):
        super().__init__()
        self.parts = parts
        self.lang = lang
        self.slow = slow
        self.folder_path = folder_path
        self.signals = WorkerSignals()
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    def run(self):
        output_files = []
        total = len(self.parts)
        for i, part in enumerate(self.parts):
            if self.stop_flag: break
            filename = os.path.join(self.folder_path, f"{BASE_FILE_NAME_DETAIL}{i+1}.mp3")
            if not os.path.exists(filename):
                try:
                    time.sleep(0.8)
                    tts = gTTS(text=part, lang=self.lang, slow=self.slow)
                    tts.save(filename)
                except Exception as e:
                    if "429" in str(e) or "Too Many Requests" in str(e):
                        self.signals.error_429.emit()
                        return
            output_files.append(filename)
            self.signals.progress.emit(i + 1, total)
        self.signals.finished.emit(output_files)

class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.folder_path = os.path.join(os.getcwd(), "AmThanh_Output")
        if not os.path.exists(self.folder_path): os.makedirs(self.folder_path)
        self.threadpool = QThreadPool.globalInstance()
        self.usage_history = []
        self.setupUi(self)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 620)
        Dialog.setStyleSheet("font-family: 'Segoe UI'; font-size: 13px;")
        layout = QtWidgets.QVBoxLayout(Dialog)

        # --- BANNER ĐIỀU HƯỚNG ---
        self.btnProWeb = QtWidgets.QPushButton("🔥 DÙNG GIỌNG XỊN HƠN TẠI WEB TTS FOR FREE NHEN")
        self.btnProWeb.setStyleSheet("""
            background-color: #0984e3; color: white; font-weight: bold; 
            padding: 10px; border-radius: 5px; border: none;
        """)
        # Link Web của bạn
        self.btnProWeb.clicked.connect(lambda: QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://ttsforfree.com/vi/")))
        layout.addWidget(self.btnProWeb)

        # Quota Group
        quota_group = QtWidgets.QGroupBox("Hạn mức gTTS (Miễn phí)")
        q_lay = QtWidgets.QVBoxLayout(quota_group)
        self.lbl_quota = QtWidgets.QLabel("Đã dùng: 0 / 60,000 ký tự (Thường là 1 giờ được nhiêu đây ký tự)")
        self.lbl_quota.setStyleSheet("font-weight: bold; color: #27ae60;")
        q_lay.addWidget(self.lbl_quota)
        layout.addWidget(quota_group)

        # Input
        top_layout = QtWidgets.QHBoxLayout()
        self.label_chars = QtWidgets.QLabel("Characters: 0")
        self.label_parts = QtWidgets.QLabel("Parts: 0")
        top_layout.addWidget(self.label_chars)
        top_layout.addWidget(self.label_parts)
        layout.addLayout(top_layout)

        self.textInput = QtWidgets.QTextEdit()
        self.textInput.setPlaceholderText("Nhập nội dung cần chuyển đổi...")
        layout.addWidget(self.textInput)

        # Settings
        settings_group = QtWidgets.QGroupBox("Cài đặt")
        grid = QtWidgets.QGridLayout(settings_group)
        self.comboBoxLang = QtWidgets.QComboBox()
        all_langs = lang.tts_langs()
        for code, name in sorted(all_langs.items(), key=lambda x: x[1]):
            self.comboBoxLang.addItem(name, code)
        idx_vi = self.comboBoxLang.findData("vi")
        if idx_vi >= 0: self.comboBoxLang.setCurrentIndex(idx_vi)
        
        grid.addWidget(QtWidgets.QLabel("Ngôn ngữ:"), 0, 0)
        grid.addWidget(self.comboBoxLang, 0, 1)
        self.checkSlow = QtWidgets.QCheckBox("Đọc chậm")
        grid.addWidget(self.checkSlow, 1, 1)
        layout.addWidget(settings_group)

        # Progress
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setVisible(False)
        layout.addWidget(self.progressBar)

        # Buttons
        btn_layout = QtWidgets.QHBoxLayout()
        self.btnPreprocess = QtWidgets.QPushButton("Làm sạch")
        self.btnStart = QtWidgets.QPushButton("Tải MP3")
        self.btnMerge = QtWidgets.QPushButton("Ghép File Pro") # Nút điều hướng
        
        self.btnStart.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold; height: 35px;")
        self.btnMerge.setStyleSheet("background-color: #6c5ce7; color: white; font-weight: bold; height: 35px;")
        
        btn_layout.addWidget(self.btnPreprocess)
        btn_layout.addWidget(self.btnStart)
        btn_layout.addWidget(self.btnMerge)
        layout.addLayout(btn_layout)

        # Events
        self.textInput.textChanged.connect(self.update_info)
        self.btnPreprocess.clicked.connect(self.preprocess_action)
        self.btnStart.clicked.connect(self.start_tts)
        self.btnMerge.clicked.connect(self.handle_merge_redirect)

    def update_info(self):
        text = self.textInput.toPlainText()
        self.label_chars.setText(f"Characters: {len(text)}")
        parts = self.split_text(text)
        self.label_parts.setText(f"Parts: {len(parts)}")
        now = datetime.now()
        self.usage_history = [h for h in self.usage_history if h[0] > now - timedelta(hours=1)]
        total_used = sum(h[1] for h in self.usage_history)
        self.lbl_quota.setText(f"Đã dùng: {total_used:,} / {CHAR_LIMIT_PER_HOUR:,} ký tự")

    def split_text(self, text, max_length=2000):
        sentences = text.split(". ")
        parts = []
        temp = ""
        for s in sentences:
            if len(temp) + len(s) < max_length: temp += s + ". "
            else:
                parts.append(temp.strip()); temp = s + ". "
        if temp: parts.append(temp.strip())
        return parts

    def preprocess_action(self):
        self.textInput.setText(format_textinput(self.textInput.toPlainText()))

    def start_tts(self):
        text = self.textInput.toPlainText()
        if not text.strip(): return
        self.usage_history.append((datetime.now(), len(text)))
        self.update_info()
        self.progressBar.setVisible(True)
        self.btnStart.setEnabled(False)
        worker = GTTSWorker(self.split_text(text), self.comboBoxLang.currentData(), self.checkSlow.isChecked(), self.folder_path)
        worker.signals.progress.connect(lambda c, t: self.progressBar.setValue(int(c/t*100)))
        worker.signals.finished.connect(self.tts_finished)
        worker.signals.error_429.connect(self.handle_429)
        self.threadpool.start(worker)

    def handle_429(self):
        self.btnStart.setEnabled(True)
        QMessageBox.critical(self, "Hết hạn IP", "Google đã chặn IP của bạn. Hãy lên Web dùng bản Pro không giới hạn!")
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://your-website.com"))

    def tts_finished(self):
        self.btnStart.setEnabled(True)
        # Mở thư mục chứa file để user thấy thành quả
        if sys.platform == 'win32': os.startfile(self.folder_path)
        QMessageBox.information(self, "Xong", "Đã tải xong các phần MP3!")

    def handle_merge_redirect(self):
        # Thông báo điều hướng khi nhấn nút Ghép File
        msg = QMessageBox(self)
        msg.setWindowTitle("Tính năng Ghép File")
        msg.setText("Để giữ App gọn nhẹ, tính năng Ghép File tự động được hỗ trợ tại Website hoặc bản Full trên GitHub.")
        msg.setInformativeText("Bạn muốn thực hiện thao tác nào?")
        
        btn_web = msg.addButton("Ghép tại Web (Nhanh)", QMessageBox.ButtonRole.AcceptRole)
        btn_git = msg.addButton("Tải bản Full (GitHub/Drive)", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("Hủy", QMessageBox.ButtonRole.RejectRole)
        
        msg.exec()
        if msg.clickedButton() == btn_web:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://your-website.com/merge"))
        elif msg.clickedButton() == btn_git:
            # Thay bằng link Drive/GitHub chứa bản có FFmpeg của bạn
            QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/your-repo/full-version"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui_Dialog()
    window.show()
    sys.exit(app.exec())