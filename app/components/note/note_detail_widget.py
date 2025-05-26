from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy
from PySide6.QtCore import Qt

from app.components.buttons.button_icon import ButtonIcon
from app.components.buttons.button_text_small import ButtonTextSmall
from app.components.labels.label_default import LabelDefault
from app.utils.layouts.flow_layout import FlowLayout
from app.components.badges.keywordbadge import KeywordBadge


class NoteDetailWidget(QFrame):
    def __init__(self, note_data, x=408, parent=None):
        super().__init__(parent)
        self.setObjectName("NoteDetailWidget")
        self.setFixedWidth(x)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)

        # --- Titre + bouton fermeture
        note_name = LabelDefault(style="H1", text=note_data.get("title", ""), x=None)
        self.note_close_button = ButtonIcon(icon_name="arrow_big_right", icon_color="white", style="Button_Orange")

        self.note_detail_top = QWidget(self)
        note_detail_top_layout = QHBoxLayout(self.note_detail_top)
        note_detail_top_layout.setSpacing(12)
        note_detail_top_layout.setContentsMargins(0, 0, 0, 0)
        note_detail_top_layout.addWidget(note_name, alignment=Qt.AlignTop | Qt.AlignLeft)
        note_detail_top_layout.addWidget(self.note_close_button, alignment=Qt.AlignTop | Qt.AlignRight)
        self.note_detail_top.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)

        # --- Contenu principal de la note
        contenu_clean = note_data.get("contenu", "").strip()
        note_contenu = LabelDefault(style="Text", text=contenu_clean, x=None)

        # --- Projet + date (sur une seule ligne)
        note_projet_label = LabelDefault(style="Text", text=note_data.get("project", ""))
        note_projet_label.setWordWrap(False)
        note_projet_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        note_date_label = LabelDefault(style="Text", text=note_data.get("date", ""))

        separator_line = QFrame()
        separator_line.setFrameShape(QFrame.VLine)
        separator_line.setFixedHeight(6)
        separator_line.setFixedWidth(1)
        separator_line.setStyleSheet("background-color: white; border: none;")

        project_date_widget = QWidget()
        project_date_layout = QHBoxLayout(project_date_widget)
        project_date_layout.setContentsMargins(0, 0, 0, 0)
        project_date_layout.setSpacing(6)
        project_date_layout.addWidget(note_projet_label)
        project_date_layout.addWidget(separator_line)
        project_date_layout.addWidget(note_date_label)
        project_date_layout.addStretch()

        # --- Mots-clés affichés en ligne
        note_keywords_widget = QWidget()
        note_keywords_layout = FlowLayout(note_keywords_widget, spacing=6)
        for keyword in note_data.get("keywords", []):
            badge = KeywordBadge(text=keyword)
            badge.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            note_keywords_layout.addWidget(badge)

        # --- Description
        note_description = LabelDefault(style="Text", text=note_data.get("description", ""))

        # --- "Voir plus d'info" + détails
        note_more_button = ButtonTextSmall(text="plus de détails")
        note_more_button.setStyleSheet("color: #FCF7F3;")
        self.note_more_detail = QWidget(self)
        note_more_detail_layout = QVBoxLayout(self.note_more_detail)
        note_more_detail_layout.setSpacing(6)
        note_more_detail_layout.setContentsMargins(0, 0, 0, 0)
        
        note_more_detail_layout.addWidget(project_date_widget)
        note_more_detail_layout.addWidget(note_keywords_widget)
        note_more_detail_layout.addWidget(note_description)

        self.note_detail_bottom = QWidget(self)
        note_detail_bottom_layout = QVBoxLayout(self.note_detail_bottom)
        note_detail_bottom_layout.setSpacing(6)
        note_detail_bottom_layout.setContentsMargins(0, 0, 0, 0)
        note_detail_bottom_layout.addWidget(note_more_button)
        note_detail_bottom_layout.addWidget(self.note_more_detail)

        # --- Layout principal
        note_detail_layout = QVBoxLayout(self)
        note_detail_layout.setSpacing(24)
        note_detail_layout.setContentsMargins(16, 16, 16, 16)
        note_detail_layout.addWidget(self.note_detail_top)
        note_detail_layout.addWidget(note_contenu)
        note_detail_layout.addWidget(self.note_detail_bottom)

        # --- Interaction
        self.note_close_button.clicked.connect(self.close_parent_detail)

        self.adjustSize()

    def close_parent_detail(self):
        if self.parent():
            self.parent().close_note_detail()
