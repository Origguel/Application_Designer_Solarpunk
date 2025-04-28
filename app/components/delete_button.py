
from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

class DeleteButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setText("-")
        self.setObjectName("DeleteButton")
        self.setFixedSize(36, 36)
        self.setCursor(Qt.PointingHandCursor)
