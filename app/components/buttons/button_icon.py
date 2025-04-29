from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Qt

class ButtonIcon(QPushButton):
    def __init__(self, text="+", x=36, y=36, style="Button_Primary", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setFixedSize(x, y)
        self.setObjectName(style)
        self.setCursor(Qt.PointingHandCursor)
