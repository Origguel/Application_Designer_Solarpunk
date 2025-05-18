from PySide6.QtWidgets import QLabel

class LabelDefault(QLabel):
    def __init__(self ,text="Texte du bouton", style="Label_Default", x=376, y=32, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(style)
        self.setFixedHeight(y)
        self.setFixedWidth(x)