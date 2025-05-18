from PySide6.QtWidgets import QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class ButtonText(QPushButton):
    def __init__(self, text="Texte du bouton", style="Button_Medium", x=94, y=32, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(style)
        self.setCursor(Qt.PointingHandCursor)

        self.setFixedHeight(y)
        self.setFixedWidth(x)

