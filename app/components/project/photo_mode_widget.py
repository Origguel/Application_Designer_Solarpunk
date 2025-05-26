# app/components/project/photo/photo_mode_widget.py

from PySide6.QtWidgets import QWidget, QLabel, QGridLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os

class PhotoModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("PhotoModeWidget")

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(16)
        self.layout.setVerticalSpacing(16)

        self.setLayout(self.layout)
        self.setVisible(False)

        self.load_photos()

    def load_photos(self):
        fake_image_paths = [
            "data\projets\Photos\projet_0001\0001.png", 
            "data\projets\Photos\projet_0001\0002.png",
            "data\projets\Photos\projet_0001\0003.png"
        ]

        for i, path in enumerate(fake_image_paths):
            label = QLabel()
            label.setFixedSize(443, 266)
            label.setStyleSheet("background-color: #F0F0F0; border-radius: 6px;")
            label.setScaledContents(True)
            if os.path.exists(path):
                pixmap = QPixmap(path)
                label.setPixmap(pixmap)
            else:
                label.setText("📸")
                label.setAlignment(Qt.AlignCenter)
            row = i // 2
            col = i % 2
            self.layout.addWidget(label, row, col)
