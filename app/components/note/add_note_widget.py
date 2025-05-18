# app/components/add_note_widget.py

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt, Signal
from app.components.note.note_creator import NoteCreator
from datetime import datetime

from app.utils.categorie_manager.category_tree_updater import CategoryTreeUpdater

# Components
from app.components.dropdowns.dropdown_default import Dropdown_Default
from app.components.buttons.button_text import ButtonText
from app.components.inputs.input_default import Input_Default
from app.components.inputs.input_multiline import Input_Multiline



class AddNoteWidget(QWidget):
    cancelled = Signal()
    note_created = Signal(str, list)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("AddNoteWidget")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(36, 36, 36, 36)
        self.layout.setSpacing(48)

        self.setup_left_panel()
        self.setup_right_panel()

    def setup_left_panel(self):
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(12)


        self.title_input = Input_Default(placeholder="Titre de la note")

        self.date_input = Input_Default(placeholder="Date de création de la note")
        today = datetime.now().strftime("%d/%m/%Y")
        self.date_input.setText(today)

        self.type_selector = Dropdown_Default(style="Dropdown_Default", items=["Texte", "Image", "Code", "Lien"], responsive=True, parent=self)

        self.project_selector = Dropdown_Default(style="Dropdown_Default", items=["Projet 1", "Projet 2", "Projet 3", "Projet 4"], responsive=True, parent=self)

        self.description_input = Input_Multiline(placeholder="Description rapide de la note", x=True, y=True, parent=self)

        # Bouton Annuler
        self.cancel_button = ButtonText("Annuler", 120, 36, self)
        self.cancel_button.clicked.connect(self.cancelled.emit)

        # Ajout des widgets
        self.left_layout.addWidget(self.title_input)
        self.left_layout.addWidget(self.date_input)
        self.left_layout.addWidget(self.type_selector)
        self.left_layout.addWidget(self.project_selector)
        self.left_layout.addWidget(self.description_input)

        # Layout pour bouton Annuler
        self.cancel_layout = QHBoxLayout()
        self.cancel_layout.setContentsMargins(0, 0, 0, 0)
        self.cancel_layout.setAlignment(Qt.AlignLeft)  # aligne tout le layout à gauche
        self.cancel_layout.addWidget(self.cancel_button)
        self.left_layout.addLayout(self.cancel_layout)


        self.layout.addWidget(self.left_panel)

    def setup_right_panel(self):
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(12)
        self.setObjectName("AddNoteWidget")

        self.contenu_editor = Input_Multiline(placeholder="Contenu principal de la note", x=True, y=True, parent=self)

        # Bouton Valider
        self.validate_button = ButtonText("Valider", 120, 36, self)
        self.validate_button.clicked.connect(self.cancelled.emit)
        self.validate_button.clicked.connect(self.validate_and_save_note)

        self.right_layout.addWidget(self.contenu_editor)

        # Layout pour bouton Valider
        self.validate_layout = QHBoxLayout()
        self.validate_layout.setContentsMargins(0, 0, 0, 0)
        self.validate_layout.setAlignment(Qt.AlignRight)  # aligne tout le layout à gauche
        self.validate_layout.addWidget(self.validate_button)
        self.right_layout.addLayout(self.validate_layout)

        self.layout.addWidget(self.right_panel)

    def clear_fields(self):
        self.title_input.clear()
        self.date_input.clear()
        self.description_input.clear()
        self.contenu_editor.clear()
        self.type_selector.setCurrentIndex(0)
        self.project_selector.setCurrentIndex(0)

    def validate_and_save_note(self):
        """Quand on clique sur Valider ➔ Création du fichier de note"""
        title = self.title_input.text().strip()
        date = self.date_input.text().strip()
        project = self.project_selector.currentText().strip()
        description = self.description_input.toPlainText().strip()
        contenu = self.contenu_editor.toPlainText().strip()
        type_note = self.type_selector.currentText().strip()

        if not title or not date or not project:
            print("❗ Tous les champs obligatoires ne sont pas remplis.")
            return

        # Créer la note
        note_data = NoteCreator.create_note(
            title=title,
            date_str=date,
            note_type=type_note,
            project=project,
            description=description,
            contenu=contenu
        )

        print(f"✅ Note '{title}' enregistrée avec succès !")

        self.clear_fields()
        self.note_created.emit(note_data["id"], note_data["keywords"])
        self.cancelled.emit()
