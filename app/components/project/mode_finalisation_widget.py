from PySide6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QVBoxLayout
from PySide6.QtCore import Qt
from app.components.inputs.input_multiline import Input_Multiline
from app.components.labels.label_default import LabelDefault

class Mode_Finalisation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # 🔹 Bloc 1
        self.moyendaction_label = LabelDefault(text="Moyens d’action", style="H2_WB", x=384)
        self.moyendaction_input = Input_Multiline(object_name="Input_Multiline_Prisedenote", placeholder="Quelles ont été les choix et décision importante pour ce projet ?", x=384, y=True)
        self.moyendaction_widget = QWidget(self)
        self.moyendaction_layout = QVBoxLayout(self.moyendaction_widget)
        self.moyendaction_layout.setContentsMargins(0, 0, 0, 0)
        self.moyendaction_layout.setSpacing(6)
        self.moyendaction_layout.addWidget(self.moyendaction_label)
        self.moyendaction_layout.addWidget(self.moyendaction_input)

        # 🔹 Bloc 2
        self.resultante_label = LabelDefault(text="Résultantes", style="H2_WB", x=384)
        self.resultante_input = Input_Multiline(object_name="Input_Multiline_Prisedenote", placeholder="Quelles en ont été les répercussions ?", x=384, y=True)
        self.resultante_widget = QWidget(self)
        self.resultante_layout = QVBoxLayout(self.resultante_widget)
        self.resultante_layout.setContentsMargins(0, 0, 0, 0)
        self.resultante_layout.setSpacing(6)
        self.resultante_layout.addWidget(self.resultante_label)
        self.resultante_layout.addWidget(self.resultante_input)

        # 🔹 Bloc 3
        self.abstract_label = LabelDefault(text="Abstract", style="H2_WB", x=384)
        self.abstract_input = Input_Multiline(object_name="Input_Multiline_Prisedenote", placeholder="Raconte ton expérience dans ce projet, n’hésite pas à te conseiller pour de futurs projets", x=384, y=True)
        self.abstract_widget = QWidget(self)
        self.abstract_layout = QVBoxLayout(self.abstract_widget)
        self.abstract_layout.setContentsMargins(0, 0, 0, 0)
        self.abstract_layout.setSpacing(6)
        self.abstract_layout.addWidget(self.abstract_label)
        self.abstract_layout.addWidget(self.abstract_input)

        # 🔹 Layout principal
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        layout.addWidget(self.moyendaction_widget)
        layout.addWidget(self.resultante_widget)
        layout.addWidget(self.abstract_widget)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
