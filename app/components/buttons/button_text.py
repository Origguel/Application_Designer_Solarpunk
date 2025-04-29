from PySide6.QtWidgets import QPushButton, QSizePolicy
from PySide6.QtCore import Qt

class ButtonText(QPushButton):
    def __init__(self, text="+", x=36, y=36, style="Button_Primary", parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setObjectName(style)
        self.setCursor(Qt.PointingHandCursor)

        # Déterminer la taille/expansion horizontale
        if x is True:
            horizontal_policy = QSizePolicy.Expanding
        elif isinstance(x, int):
            self.setMinimumWidth(x)
            horizontal_policy = QSizePolicy.Fixed
        else:
            raise ValueError("x doit être un int (taille fixe) ou True (expansible)")

        # Déterminer la taille/expansion verticale
        if y is True:
            vertical_policy = QSizePolicy.Expanding
        elif isinstance(y, int):
            self.setMinimumHeight(y)
            vertical_policy = QSizePolicy.Fixed
        else:
            raise ValueError("y doit être un int (taille fixe) ou True (expansible)")

        self.setSizePolicy(horizontal_policy, vertical_policy)

        # Optionnel : forcer une taille initiale fixe si int
        if isinstance(x, int) and isinstance(y, int):
            self.setFixedSize(x, y)
