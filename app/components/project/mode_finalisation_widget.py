from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from app.components.inputs.input_multiline import Input_Multiline

class Mode_Finalisation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.moyendaction_input = Input_Multiline(
            object_name="Input_Multiline_Prisedenote",
            placeholder="Prise de note",
            x=384,
            y=True
        )

        self.resultante_input = Input_Multiline(
            object_name="Input_Multiline_Prisedenote",
            placeholder="Prise de note",
            x=384,
            y=True
        )

        self.abstract_input = Input_Multiline(
            object_name="Input_Multiline_Prisedenote",
            placeholder="Prise de note",
            x=384,
            y=True
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addWidget(self.moyendaction_input)
        layout.addWidget(self.resultante_input)
        layout.addWidget(self.abstract_input)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

