from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt

class ThemeModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ThemeModeWidget")
        self.label = QLabel("Mode Thématique en construction...", self)
        self.label.setAlignment(Qt.AlignCenter)
