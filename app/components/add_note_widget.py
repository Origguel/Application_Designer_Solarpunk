# app/components/add_note_widget.py

from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QComboBox
from PySide6.QtCore import Qt, Signal
from app.utils.note_creator import NoteCreator



class AddNoteWidget(QWidget):
    cancelled = Signal()
    note_created = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("AddNoteWidget")

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        self.setup_left_panel()
        self.setup_right_panel()

    def setup_left_panel(self):
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(10)

        label_style = "QLabel { border: none; color: #2B2B2B; font-weight: bold; }"

        # Champs de gauche
        self.title_label = QLabel("Titre:")
        self.title_label.setStyleSheet(label_style)
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Titre de la note")

        self.date_label = QLabel("Date:")
        self.date_label.setStyleSheet(label_style)
        self.date_input = QLineEdit()
        self.date_input.setPlaceholderText("Date (ex: 26/04/2025)")

        # 🆕 Remplir automatiquement avec la date d'aujourd'hui
        from datetime import datetime
        today = datetime.now().strftime("%d/%m/%Y")
        self.date_input.setText(today)


        self.type_label = QLabel("Type:")
        self.type_label.setStyleSheet(label_style)
        self.type_selector = QComboBox()
        self.type_selector.addItems(["texte"])

        self.project_label = QLabel("Projet:")
        self.project_label.setStyleSheet(label_style)
        self.project_selector = QComboBox()
        self.project_selector.addItems(["default"])

        self.description_label = QLabel("Description:")
        self.description_label.setStyleSheet(label_style)
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description rapide de la note")

        # Bouton Annuler
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.setObjectName("SecondaryButton")
        self.cancel_button.setFixedSize(120, 40)
        self.cancel_button.clicked.connect(self.cancelled.emit)

        # Ajout des widgets
        self.left_layout.addWidget(self.title_label)
        self.left_layout.addWidget(self.title_input)
        self.left_layout.addWidget(self.date_label)
        self.left_layout.addWidget(self.date_input)
        self.left_layout.addWidget(self.type_label)
        self.left_layout.addWidget(self.type_selector)
        self.left_layout.addWidget(self.project_label)
        self.left_layout.addWidget(self.project_selector)
        self.left_layout.addWidget(self.description_label)
        self.left_layout.addWidget(self.description_input)

        # Layout pour bouton Annuler
        self.cancel_layout = QHBoxLayout()
        self.cancel_layout.addStretch()
        self.cancel_layout.addWidget(self.cancel_button)
        self.cancel_layout.addStretch()
        self.left_layout.addLayout(self.cancel_layout)

        self.layout.addWidget(self.left_panel)

    def setup_right_panel(self):
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(10)

        self.contenu_editor = QTextEdit()
        self.contenu_editor.setPlaceholderText("Contenu principal de la note...")

        # Bouton Valider
        self.validate_button = QPushButton("Valider")
        self.validate_button.setObjectName("PrimaryButton")
        self.validate_button.setFixedSize(120, 40)
        self.validate_button.clicked.connect(self.validate_and_save_note)

        self.right_layout.addWidget(self.contenu_editor)

        # Layout pour bouton Valider
        self.validate_layout = QHBoxLayout()
        self.validate_layout.addStretch()
        self.validate_layout.addWidget(self.validate_button)
        self.validate_layout.addStretch()
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

        NoteCreator.create_note(
            title=title,
            date_str=date,
            note_type=type_note,
            project=project,
            description=description,
            contenu=contenu
        )

        print(f"✅ Note '{title}' enregistrée avec succès !")

        self.clear_fields()
        self.note_created.emit()
        self.cancelled.emit()
