# app/components/note_detail_widget.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QSizePolicy, QHBoxLayout
from PySide6.QtCore import Qt

class NoteDetailWidget(QFrame):
    def __init__(self, note_data, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setObjectName("NoteDetailWidget")
        self.setStyleSheet("background-color: #FFFFFF;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # 🧹 Bouton Supprimer supprimé pour test

        # Infos de la note
        title = QLabel(f"<b>{note_data.get('title', '')}</b>")
        title.setObjectName("NoteTitle")

        project = QLabel(f"Projet : {note_data.get('project', '-')}")
        project.setObjectName("NoteProject")

        date = QLabel(f"Date : {note_data.get('date', '-')}")
        date.setObjectName("NoteDate")

        keywords = QLabel("Mots-clés : " + ", ".join(note_data.get("keywords", [])))
        keywords.setObjectName("NoteKeywords")

        description = QLabel(note_data.get("description", ""))
        description.setObjectName("NoteDescription")

        for label in [title, project, date, keywords, description]:
            label.setWordWrap(True)
            layout.addWidget(label)

        contenu = QLabel(note_data.get("contenu", ""))
        contenu.setWordWrap(True)
        contenu.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        contenu.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        contenu.setObjectName("NoteContent")
        layout.addWidget(contenu)
