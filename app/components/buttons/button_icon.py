from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
import os

class ButtonIcon(QPushButton):
    def __init__(self, icon_name="add", style="Button_Default", parent=None):
        super().__init__(parent)

        self.setFixedSize(32, 32)
        self.setObjectName(style)
        self.setCursor(Qt.PointingHandCursor)

        icon_path = os.path.join("assets", "icons", f"{icon_name}.svg")

        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        else:
            print(f"[ButtonIcon] ❌ Fichier icône introuvable : {icon_path}")
