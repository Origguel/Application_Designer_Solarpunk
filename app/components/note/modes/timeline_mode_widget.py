from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt

class TimelineModeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("TimelineModeWidget")
        self.label = QLabel("Mode Timeline en construction...", self)
        self.label.setAlignment(Qt.AlignCenter)
