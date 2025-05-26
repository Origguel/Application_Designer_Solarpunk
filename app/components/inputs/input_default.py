from PySide6.QtWidgets import QLineEdit, QSizePolicy

class Input_Default(QLineEdit):
    def __init__(self, placeholder="Information à rentrer", object_name="Input_Research", x=230, y=32, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setObjectName(object_name)

        # Gestion responsive vs fixe
        if x is not None and y is not None:
            self.setFixedSize(x, y)
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        elif x is not None:
            self.setFixedWidth(x)
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        elif y is not None:
            self.setFixedHeight(y)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
