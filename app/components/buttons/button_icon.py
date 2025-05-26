from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
import os

class ButtonIcon(QPushButton):
    def __init__(self, icon_name="add", style="Button_Default", parent=None):
        super().__init__(parent)

        self.setFixedSize(32, 32)
        self.setCursor(Qt.PointingHandCursor)
        self.icon_name = icon_name
        self.setObjectName(style)

        self.update_icon()

    def update_icon(self):
        style = self.objectName()
        if "Selected" in style:
            print("icon_white")
            icon_path = os.path.join("assets", "icons", "white", f"{self.icon_name}.svg")
        else:
            print("icon_black")
            icon_path = os.path.join("assets", "icons", "black", f"{self.icon_name}.svg")

        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(24, 24))
        else:
            print(f"[ButtonIcon] ❌ Fichier icône introuvable : {icon_path}")
