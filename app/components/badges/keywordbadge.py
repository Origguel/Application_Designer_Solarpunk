from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt

class KeywordBadge(QLabel):
    def __init__(self, text, parent=None):
        formatted = text.strip().capitalize()  # ✅ applique AVANT le super().__init__
        super().__init__(formatted, parent)

        self.setObjectName("Keyword_Badge")
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
