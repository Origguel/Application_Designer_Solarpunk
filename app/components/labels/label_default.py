from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt

class LabelDefault(QLabel):
    def __init__(self ,text="Texte du bouton", style="Label_Default", x=376, y=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(style)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.setFixedWidth(x)

        if y is not None:
            self.setFixedHeight(y)
        else:
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)