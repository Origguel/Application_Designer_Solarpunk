from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt

class LabelDefault(QLabel):
    def __init__(self, text="Texte du bouton", style="Label_Default", x=376, y=None, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(style)
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        if x is not None:
            self.setFixedWidth(x)
            size_policy.setHorizontalPolicy(QSizePolicy.Fixed)

        if y is not None:
            self.setFixedHeight(y)
            size_policy.setVerticalPolicy(QSizePolicy.Fixed)

        self.setSizePolicy(size_policy)

        # 🔥 Important : dire à Qt que la taille dépend du contenu
        self.setMinimumSize(0, 0)
