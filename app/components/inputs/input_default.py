from PySide6.QtWidgets import QLineEdit, QSizePolicy

class Input_Default(QLineEdit):
    def __init__(self, placeholder="Information à rentrer", object_name="Input_Research", x=230, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setObjectName(object_name)

        # Taille fixe
        self.setFixedSize(x, 32)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Padding pour texte aligné "center-left"
        self.setStyleSheet("padding: 0px 10px;")
