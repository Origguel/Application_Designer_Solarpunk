from PySide6.QtWidgets import QLineEdit, QSizePolicy

class Input_Default(QLineEdit):
    def __init__(
        self,
        placeholder="Information à rentrer",
        object_name="",
        x=200,
        y=36,
        text_position="center-left",  # <--- nouveau paramètre
        parent=None
    ):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setObjectName(object_name)

        # Déterminer le policy horizontal
        if x is True:
            horizontal_policy = QSizePolicy.Expanding
            self.setMinimumWidth(150)
        elif isinstance(x, int):
            self.setFixedWidth(x)
            horizontal_policy = QSizePolicy.Fixed
        else:
            raise ValueError("x doit être un int (taille fixe) ou True (expansible)")

        # Déterminer le policy vertical
        if y is True:
            vertical_policy = QSizePolicy.Expanding
            self.setMinimumHeight(30)
        elif isinstance(y, int):
            self.setFixedHeight(y)
            vertical_policy = QSizePolicy.Fixed
        else:
            raise ValueError("y doit être un int (taille fixe) ou True (expansible)")

        self.setSizePolicy(horizontal_policy, vertical_policy)

        # Gestion du placement du texte par padding
        if text_position == "top-left":
            # simulate vertical align top by pushing text down slightly
            self.setStyleSheet("padding-top: 2px; padding-left: 10px;")
        elif text_position == "center-left":
            self.setStyleSheet("padding: 0px 10px;")
        else:
            raise ValueError("text_position doit être 'top-left' ou 'center-left'")
