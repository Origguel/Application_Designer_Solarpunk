from PySide6.QtWidgets import QWidget, QLabel, QGridLayout
from PySide6.QtGui import QPixmap, QPainter, QPainterPath
from PySide6.QtCore import Qt
import os

from app.components.buttons.button_icon import ButtonIcon

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
            "data/projets/Photos/projet_0001/0001.png", 
            "data/projets/Photos/projet_0001/0002.png",
            "data/projets/Photos/projet_0001/0003.png"
        ]

        # Ajouter les images dans la grille
        for i, path in enumerate(fake_image_paths):
            label = QLabel()
            label.setFixedSize(443, 266)
            label.setStyleSheet("border-radius: 6px; background-color: #F4B67C;")
            label.setAlignment(Qt.AlignCenter)

            if os.path.exists(path):
                original = QPixmap(path)
                scaled = original.scaled(label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

                rounded = QPixmap(label.size())
                rounded.fill(Qt.transparent)

                painter = QPainter(rounded)
                painter.setRenderHint(QPainter.Antialiasing)
                clip_path = QPainterPath()
                clip_path.addRoundedRect(0, 0, label.width(), label.height(), 6, 6)
                painter.setClipPath(clip_path)
                painter.drawPixmap(0, 0, scaled)
                painter.end()

                label.setPixmap(rounded)
            else:
                label.setText("📸")

            row = i // 2
            col = i % 2
            self.layout.addWidget(label, row, col)

        # Ajouter le bouton d'ajout en dernier
        total_photos = len(fake_image_paths)
        row = total_photos // 2
        col = total_photos % 2

        add_button = ButtonIcon(icon_name="image", icon_color="black", style="Button_Medium", x=443, y=266)
        self.layout.addWidget(add_button, row, col)
