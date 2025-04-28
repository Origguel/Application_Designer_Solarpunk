# app/components/plus_button.py

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

class ResetViewButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("R")
        self.setFixedSize(36, 36)
        self.setObjectName("PlusButton")
        self.setCursor(Qt.PointingHandCursor)
