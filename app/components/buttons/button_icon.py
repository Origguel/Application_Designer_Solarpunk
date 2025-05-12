from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
import os

class ButtonIcon(QPushButton):
    def __init__(self, icon_name="add", x=30, y=30, style="Button_Primary", parent=None):
        super().__init__(parent)

        self.setFixedSize(x, y)
        self.setObjectName(style)
        self.setCursor(Qt.PointingHandCursor)

        icon_path = os.path.join("assets", "icons", f"{icon_name}.svg")

        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(x - 8, y - 8))  # Marges internes
        else:
            print(f"[ButtonIcon] ❌ Fichier icône introuvable : {icon_path}")
