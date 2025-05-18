from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt

from app.components.buttons.button_icon import ButtonIcon
from app.utils.layouts.flow_layout import FlowLayout

class NoteDetailWidget(QFrame):
    def __init__(self, note_data, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setObjectName("NoteDetailWidget")
        layout = QVBoxLayout(self)

        self.close_button = ButtonIcon(icon_name="arrow_big_Left", parent=self)
        self.close_button.move(460 - 30 - 3, 3)
        self.close_button.clicked.connect(self.close_detail)
        
        layout.setContentsMargins(6, 30 + 6 + 6, 6, 6)
        layout.setSpacing(8)

        # 🧹 Bouton Supprimer supprimé pour test

        # Infos de la note
        title = QLabel(f"<b>{note_data.get('title', '')}</b>")
        title.setObjectName("NoteTitle")

        project = QLabel(f"Projet : {note_data.get('project', '-')}")
        project.setObjectName("NoteProject")

        date = QLabel(f"Date : {note_data.get('date', '-')}")
        date.setObjectName("NoteDate")

        # Groupe des mots-clés
        keywords_widget = QWidget(self)
        keywords_layout = FlowLayout(keywords_widget, spacing=6)
        keywords_layout.setSpacing(6)
        keywords_layout.setContentsMargins(0, 0, 0, 0)

        for kw in note_data.get("keywords", []):
            pill = QLabel(kw)
            pill.setObjectName("KeywordPill")
            keywords_layout.addWidget(pill)

        description = QLabel(note_data.get("description", ""))
        description.setObjectName("NoteDescription")

        for label in [title, project, date]:
            label.setWordWrap(True)
            layout.addWidget(label)

        layout.addWidget(keywords_widget)

        description.setWordWrap(True)
        layout.addWidget(description)


        contenu = QLabel(note_data.get("contenu", ""))
        contenu.setWordWrap(True)
        contenu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contenu.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        contenu.setObjectName("NoteContent")
        layout.addWidget(contenu)

    def close_detail(self):
        if self.parent():
            self.parent().close_note_detail()