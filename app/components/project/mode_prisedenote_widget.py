from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from app.components.inputs.input_multiline import Input_Multiline

class Mode_Prisedenote(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.prisedenote_input = Input_Multiline(
            object_name="Input_Multiline_Prisedenote",
            placeholder="Prise de note",
            x=384,
            y=True
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.prisedenote_input)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

