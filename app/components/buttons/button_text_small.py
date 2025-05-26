from PySide6.QtWidgets import QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class ButtonTextSmall(QPushButton):
    def __init__(self, text="Texte du bouton", style="Button_Text_Small", x=80, y=13, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(style)
        self.setCursor(Qt.PointingHandCursor)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.adjustSize()

