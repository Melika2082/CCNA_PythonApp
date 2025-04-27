import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QListWidget, QLabel, QHBoxLayout
)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QFont

class WelcomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.setWindowTitle("🎓CCNA آموزش")
        self.setGeometry(300, 200, 500, 350)
        self.setStyleSheet("background-color: #2c3e50;")

        self.label = QLabel("آموزش CCNA", self)
        self.label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #f39c12; padding: 40px;")

        self.sub_label = QLabel("همراه با زبان اشاره", self)
        self.sub_label.setFont(QFont("Arial", 22, QFont.Weight.Normal))
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sub_label.setStyleSheet("color: orange; padding: 10px;")

        self.enter_button = QPushButton("🚀 ورود")
        self.enter_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: black;
                padding: 12px 24px;
                border: none;
                border-radius: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: white;
            }
        """)
        self.enter_button.clicked.connect(self.show_main_window)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.sub_label)
        layout.addWidget(self.enter_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)

        self.main_window = main_window

    def show_main_window(self):
        self.main_window.show()
        self.close()


class VideoWindow(QWidget):
    def __init__(self, video_file, main_window):
        super().__init__()
        self.setWindowTitle("🎬 پخش ویدیو - آموزش CCNA")
        self.setStyleSheet("background-color: #001f3f; color: white;")

        self.video_widget = QVideoWidget()
        self.video_widget.setStyleSheet("border: 2px solid white; border-radius: 10px;")

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()

        self.player.setAudioOutput(self.audio_output)
        self.player.setVideoOutput(self.video_widget)
        self.player.setSource(QUrl.fromLocalFile(video_file))

        self.play_button = QPushButton("▶ پخش")
        self.play_button.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; border-radius: 5px;")
        self.play_button.clicked.connect(self.player.play)

        self.pause_button = QPushButton("⏸ توقف")
        self.pause_button.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px; border-radius: 5px;")
        self.pause_button.clicked.connect(self.player.pause)

        self.back_button = QPushButton("🔙 بازگشت به فهرست")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 10px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #f39c12;
            }
        """)
        self.back_button.clicked.connect(self.back_to_main)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.back_button)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.main_window = main_window

        self.player.play()

    def back_to_main(self):
        self.close()  # بستن پنجره ویدیو
        self.main_window.show()  # نمایش مجدد پنجره اصلی

    def closeEvent(self, event):
        # آزادسازی منابع پلیر هنگام بستن پنجره
        self.player.stop()
        self.player.deleteLater()
        self.audio_output.deleteLater()
        event.accept()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("پارسا نمازی 📽️📚 CCNA آموزش")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #2c3e50; color: white; font-size: 14px;")

        layout = QVBoxLayout()

        self.video_list = QListWidget()
        self.video_list.addItem("📌 فصل ۱")
        self.video_list.addItem("📌 فصل ۲")
        self.video_list.addItem("📌 فصل ۳")
        self.video_list.setStyleSheet("background-color: #34495e; color: white; padding: 5px; border-radius: 8px;")
        self.video_list.clicked.connect(self.open_video_window)
        layout.addWidget(self.video_list)

        self.developer_label = QLabel("برنامه نویس: پارسا نمازی و ملیکا مردانی")
        self.developer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.developer_label.setStyleSheet("color: orange; font-size: 17px; padding: 10px;")
        layout.addWidget(self.developer_label)

        self.setLayout(layout)

        # مسیر ویدیوها
        script_dir = os.path.dirname(os.path.abspath(__file__))
        videos_dir = os.path.join(script_dir, "videos")
        self.video_files = [
            os.path.join(videos_dir, "video1.mp4"),
            os.path.join(videos_dir, "video2.mp4"),
            os.path.join(videos_dir, "video3.mp4")
        ]

    def open_video_window(self):
        index = self.video_list.currentRow()
        if index < len(self.video_files):
            self.video_window = VideoWindow(self.video_files[index], self)
            self.video_window.showFullScreen()
            self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    welcome_screen = WelcomeScreen(main_window)
    welcome_screen.show()
    sys.exit(app.exec())
