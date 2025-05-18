from PySide6.QtWidgets import QTextEdit, QSizePolicy
from PySide6.QtGui import QTextOption
from PySide6.QtCore import Qt

class Input_Multiline(QTextEdit):
    def __init__(self, placeholder="", object_name="Input_Multiline", x=128, y=64, parent=None):
        super().__init__(parent)

        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder)
        self.setAcceptRichText(False)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        # Gestion responsive ou fixe
        if x is True:
            horizontal_policy = QSizePolicy.Expanding
            self.setMinimumWidth(128)
        elif isinstance(x, int):
            self.setFixedWidth(x)
            horizontal_policy = QSizePolicy.Fixed
        else:
            raise ValueError("x doit être un int ou True")

        if y is True:
            vertical_policy = QSizePolicy.Expanding
            self.setMinimumHeight(64)
        elif isinstance(y, int):
            self.setFixedHeight(y)
            vertical_policy = QSizePolicy.Fixed
        else:
            raise ValueError("y doit être un int ou True")

        self.setSizePolicy(horizontal_policy, vertical_policy)