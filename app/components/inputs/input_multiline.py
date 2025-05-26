from PySide6.QtWidgets import QTextEdit, QSizePolicy
from PySide6.QtGui import QTextOption
from PySide6.QtCore import Qt

class Input_Multiline(QTextEdit):
    def __init__(self, placeholder="", object_name="Input_Multiline", x=128, y=True, parent=None):
        super().__init__(parent)

        self.setObjectName(object_name)
        self.setPlaceholderText(placeholder)
        self.setAcceptRichText(False)
        self.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # Gestion largeur
        if x is True:
            self.setMinimumWidth(128)
            horizontal_policy = QSizePolicy.Expanding
        elif isinstance(x, int):
            self.setFixedWidth(x)
            horizontal_policy = QSizePolicy.Fixed
        else:
            raise ValueError("x doit être un int ou True")

        # Hauteur minimum et maximum
        self._min_height = 64
        self._max_height = 600  # ou None si tu veux pas limiter
        self.setMinimumHeight(self._min_height)

        self.setSizePolicy(horizontal_policy, QSizePolicy.Fixed)

        # Connecte la fonction de resize
        self.textChanged.connect(self.auto_resize)
        self.auto_resize()  # appel initial

    def auto_resize(self):
        # Calcul de la hauteur nécessaire
        doc_height = self.document().size().height()
        margins = self.contentsMargins().top() + self.contentsMargins().bottom()
        frame = self.frameWidth() * 2
        total_height = int(doc_height + margins + frame + 4)  # padding de sécurité

        # Clamp entre min et max
        total_height = max(self._min_height, total_height)
        if self._max_height:
            total_height = min(self._max_height, total_height)

        self.setFixedHeight(total_height)
