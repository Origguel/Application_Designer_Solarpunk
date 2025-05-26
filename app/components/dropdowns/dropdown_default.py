from PySide6.QtWidgets import QComboBox, QSizePolicy
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import os


class Dropdown_Default(QComboBox):
    def __init__(self, x=200, y=32, icon_name="arrow_big_down", style="Dropdown_Default", items=None, parent=None):
        super().__init__(parent)
        self.setObjectName(style)
        self.setFixedSize(x, y)

        if items is None:
            items = ["choix 1", "choix 2", "choix 3", "choix 4"]
        self.addItems(items)

        icon_path = os.path.join("assets/icons/white/", f"{icon_name}.svg")

        if os.path.exists(icon_path):
            self.setStyleSheet(f"""
                QComboBox::down-arrow {{
                    image: url({icon_path});
                }}
            """)

        else:
            print(f"[Dropdown_Default] ❌ Fichier icône introuvable : {icon_path}")
