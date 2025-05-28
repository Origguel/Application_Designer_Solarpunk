from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt

from app.components.labels.label_default import LabelDefault


class Mode_Notation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)

        self.note_widget_ecologie = self.create_note_widget("0/10", "en Ecologie")
        self.note_widget_durabilite = self.create_note_widget("0/10", "en Durabilité")
        self.note_widget_relationnel = self.create_note_widget("0/10", "en Relationnel")
        self.note_widget_apprentissage = self.create_note_widget("0/10", "en Apprentissage")
        self.note_widget_solarpunk = self.create_note_widget("0/10", "en Design Solarpunk", note_style="Notation_Solarpunk")

        layout.addWidget(self.note_widget_ecologie, alignment=Qt.AlignTop)
        layout.addWidget(self.note_widget_durabilite, alignment=Qt.AlignTop)
        layout.addWidget(self.note_widget_relationnel, alignment=Qt.AlignTop)
        layout.addWidget(self.note_widget_apprentissage, alignment=Qt.AlignTop)
        layout.addWidget(self.note_widget_solarpunk, alignment=Qt.AlignTop)

    def create_note_widget(self, note_text, title_text, note_style="H1_WNB"):
        note_label = LabelDefault(text=note_text, style=note_style, x=None)
        title_label = LabelDefault(text=title_text, style="H2_WNB", x=None)

        note_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        title_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        widget = QWidget(self)
        widget.setMinimumWidth(224)
        widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        widget.setObjectName("Note_Layout")

        layout = QVBoxLayout(widget)
        layout.setContentsMargins(6, 32, 6, 32)
        layout.setSpacing(6)
        layout.addStretch()
        layout.addWidget(note_label, alignment=Qt.AlignCenter)
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        layout.addStretch()

        return widget
