from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt

from app.components.labels.label_default import LabelDefault
from app.components.buttons.button_text import ButtonText
from app.components.inputs.input_multiline import Input_Multiline

class PriseDeNote(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)  # ✅ 1 seul layout principal
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # -------- TOP LAYOUT --------
        title_label = LabelDefault(text="Pulp'Cycle", style="H1_WB")
        client_label = LabelDefault(text="Google", style="H2_WB", x=None)
        client_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        date_label = LabelDefault(text="Du 6 janvier 2025 au 23 mai 2025", style="Sous_Text_WB", x=256)
        date_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.see_note_button = ButtonText(text="Voir les notes de Pulp’Cycle", x=173)

        client_date_widget = QWidget()
        client_date_total_width = (client_label.sizeHint().width() + 12 + date_label.sizeHint().width())
        client_date_widget.setFixedWidth(client_date_total_width)
        client_date_widget_layout = QHBoxLayout(client_date_widget)
        client_date_widget_layout.setContentsMargins(0, 0, 0, 0)
        client_date_widget_layout.addWidget(client_label)
        client_date_widget_layout.addSpacing(12)
        client_date_widget_layout.addWidget(date_label)

        top_widget_left = QWidget()
        top_widget_left_layout = QVBoxLayout(top_widget_left)
        top_widget_left_layout.setContentsMargins(0, 0, 0, 0)
        top_widget_left_layout.setSpacing(6)
        top_widget_left_layout.addWidget(title_label)
        top_widget_left_layout.addWidget(client_date_widget)

        top_widget = QWidget()
        top_widget.setFixedHeight(50)
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(6)
        top_layout.addWidget(top_widget_left, alignment=Qt.AlignBottom)
        top_layout.addWidget(self.see_note_button , alignment=Qt.AlignBottom)

        # -------- BOTTOM LAYOUT --------
        self.prisedenote_input = Input_Multiline(object_name="Input_Multiline_Prisedenote", placeholder="Prise de note", x=True, y=True)
        bottom_widget = QWidget()
        bottom_widget.setObjectName("PriseDeNote")
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(16, 16, 16, 16)
        bottom_layout.addWidget(self.prisedenote_input)

        # -------- ASSEMBLAGE --------
        layout.addWidget(top_widget)
        layout.addWidget(bottom_widget)
