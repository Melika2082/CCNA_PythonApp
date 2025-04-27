import sys
import os
import pysrt  # برای خواندن فایل‌های زیرنویس
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QLabel, QHBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, QTimer, Qt
from PyQt6.QtGui import QFont

class WelcomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("🎓 CCNA آموزش")
        self.setGeometry(300, 200, 500, 300)
        self.setStyleSheet("background-color: #2c3e50; color: white;")
        
        self.label = QLabel("آموزش CCNA", self)
        self.label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #f39c12; padding: 50px;")
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.main_window = main_window
        QTimer.singleShot(3000, self.show_main_window)  # بعد از 3 ثانیه، صفحه اصلی نمایش داده شود

    def show_main_window(self):
        self.main_window.show()
        self.close()

class VideoWindow(QWidget):
    def __init__(self, video_file, subtitle_file):
        super().__init__()
        self.setWindowTitle("پارسا نمازی 🎬CCNA پخش ویدیو - آموزش")
        self.setGeometry(200, 150, 900, 600)
        self.setStyleSheet("background-color: #2c3e50; color: white;")

        # نمایش ویدیو
        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("border: 2px solid white; border-radius: 10px;")
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(video_file))

        # زیرنویس
        self.subtitle_label = QLabel("🔠 زیرنویس در اینجا نمایش داده می‌شود")
        self.subtitle_label.setStyleSheet("font-size: 18px; color: #f1c40f; background-color: black; padding: 10px; border-radius: 5px;")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # دکمه‌های کنترل ویدیو
        self.play_button = QPushButton("▶ پخش")
        self.play_button.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; border-radius: 5px;")
        self.play_button.clicked.connect(self.player.play)

        self.pause_button = QPushButton("⏸ توقف")
        self.pause_button.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; border-radius: 5px;")
        self.pause_button.clicked.connect(self.player.pause)

        # چیدمان دکمه‌ها
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)

        # چیدمان کلی
        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.subtitle_label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # بارگذاری زیرنویس
        self.subtitles = []
        self.subtitle_timer = QTimer(self)
        self.subtitle_timer.timeout.connect(self.update_subtitle)
        self.load_subtitle(subtitle_file)
        self.subtitle_timer.start(500)
        self.player.play()

    def load_subtitle(self, subtitle_file):
        try:
            self.subtitles = pysrt.open(subtitle_file)
        except Exception:
            self.subtitles = []
            self.subtitle_label.setText("زیرنویس یافت نشد ⚠ محل قرارگیری زیرنویس ")

    def update_subtitle(self):
        if not self.subtitles:
            return
        current_time = self.player.position()
        for sub in self.subtitles:
            start_time = (sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds) * 1000 + sub.start.milliseconds
            end_time = (sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds) * 1000 + sub.end.milliseconds
            if start_time <= current_time <= end_time:
                self.subtitle_label.setText(sub.text)
                return
        self.subtitle_label.setText("")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📚 CCNA آموزش")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2c3e50; color: white; font-size: 14px;")

        self.video_list = QListWidget()
        self.video_list.addItem("📌 فصل ۱")
        self.video_list.addItem("📌 فصل ۲")
        self.video_list.addItem("📌 فصل ۳")
        self.video_list.setStyleSheet("background-color: #34495e; color: white; padding: 5px; border-radius: 8px;")
        self.video_list.clicked.connect(self.open_video_window)
        
        self.developer_label = QLabel("برنامه نویس: پارسا نمازی و ملیکا مردانی")
        self.developer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.developer_label.setStyleSheet("color: #f39c12; font-size: 17px; padding: 10px;")

        layout = QVBoxLayout()
        layout.addWidget(self.video_list)
        layout.addWidget(self.developer_label)
        self.setLayout(layout)

        # مسیر فیلم‌ها و زیرنویس‌ها
        script_dir = os.path.dirname(os.path.abspath(__file__))  # دایرکتوری اسکریپت
        videos_dir = os.path.join(script_dir, "videos")  # پوشه فیلم‌ها

        self.video_files = [
            os.path.join(videos_dir, "video1.mp4"),
            os.path.join(videos_dir, "video2.mp4"),
            os.path.join(videos_dir, "video3.mp4")
        ]
        self.subtitle_files = [
            os.path.join(videos_dir, "video1.srt"),
            os.path.join(videos_dir, "video2.srt"),
            os.path.join(videos_dir, "video3.srt")
        ]

    def open_video_window(self):
        index = self.video_list.currentRow()
        if index < len(self.video_files):
            self.video_window = VideoWindow(self.video_files[index], self.subtitle_files[index])
            self.video_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    welcome_screen = WelcomeScreen(main_window)
    welcome_screen.show()
    sys.exit(app.exec())
