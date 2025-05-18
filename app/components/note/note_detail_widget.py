from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt

from app.components.buttons.button_icon import ButtonIcon
from app.components.buttons.button_text_small import ButtonTextSmall
from app.components.labels.label_default import LabelDefault
from app.utils.layouts.flow_layout import FlowLayout

class NoteDetailWidget(QFrame):
    def __init__(self, note_data, x=408, y=500, parent=None):
        super().__init__(parent)
        self.setObjectName("NoteDetailWidget")
        self.setFixedWidth(x)
        self.setFixedHeight(y)

        note_name = LabelDefault(style="H1", text=note_data.get("title", ""), x=330)
        self.note_close_button = ButtonIcon(icon_name="arrow_big_right", style="Button_Orange")
        note_contenu = LabelDefault(style="Text", text=note_data.get("contenu", ""))
        note_more_button = ButtonTextSmall(text="Voir plus d'information")
        note_projet = LabelDefault(style="Text", text=note_data.get("project", ""))
        note_date = LabelDefault(style="Text",text=note_data.get("date", ""))
        note_keywords = QWidget(self)
        note_keywords.setFixedHeight(20)
        note_description = LabelDefault(style="Text", text=note_data.get("description", ""))
        # Note Top
        self.note_detail_top = QWidget(self)
        self.note_detail_top.setFixedHeight(64)
        note_detail_top_layout = QHBoxLayout(self.note_detail_top)
        note_detail_top_layout.setSpacing(12)
        note_detail_top_layout.setContentsMargins(0, 0, 0, 0)
        note_detail_top_layout.addWidget(note_name, alignment=Qt.AlignTop)
        note_detail_top_layout.addWidget(self.note_close_button, alignment=Qt.AlignTop)
        # Note More Detail
        self.note_more_detail = QWidget(self)
        note_more_detail_layout = QVBoxLayout(self.note_more_detail)
        note_more_detail_layout.setSpacing(6)
        note_more_detail_layout.setContentsMargins(0, 0, 0, 0)
        note_more_detail_layout.addWidget(note_projet)
        note_more_detail_layout.addWidget(note_date)
        note_more_detail_layout.addWidget(note_keywords)
        note_more_detail_layout.addWidget(note_description)
        # Note Bottom
        self.note_detail_bottom = QWidget(self)
        self.note_detail_bottom.setFixedHeight(128)
        note_detail_bottom_layout = QVBoxLayout(self.note_detail_bottom)
        note_detail_bottom_layout.setSpacing(12)
        note_detail_bottom_layout.setContentsMargins(0, 0, 0, 0)
        note_detail_bottom_layout.addWidget(note_more_button)
        note_detail_bottom_layout.addWidget(self.note_more_detail)
        # Note Détail
        note_detail_layout = QVBoxLayout(self)
        note_detail_layout.setSpacing(24)
        note_detail_layout.setContentsMargins(16, 16, 16, 16)
        note_detail_layout.addWidget(self.note_detail_top)
        note_detail_layout.addWidget(note_contenu)
        note_detail_layout.addWidget(self.note_detail_bottom)
        # Note detail Button clicked
        self.note_close_button.clicked.connect(self.close_parent_detail)


    def close_parent_detail(self):
        if self.parent():
            self.parent().close_note_detail()