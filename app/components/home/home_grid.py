# app/components/home_grid.py
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QSizePolicy, QLabel, QFrame
from PySide6.QtCore import Signal
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap


# Componenents
from app.components.buttons.button_text import ButtonText
from app.components.buttons.button_icon import ButtonIcon



class HomeGrid(QWidget):
    # Créer un signal pour notifier le changement de page
    switch_to_notes_page = Signal()
    switch_to_projects_page = Signal()
    switch_to_stats_page = Signal()

    def __init__(self):
        super().__init__()

        # Créer un layout de type GridLayout
        self.home_layout = QGridLayout(self)
        self.home_layout.setSpacing(12)  # Espacement de 12px entre les cellules
        self.home_layout.setContentsMargins(34, 26, 34, 26)  # Marges (sauf les 0px dans home_view.py)

        # Créer 9 colonnes x 5 lignes (pour l'instant cases vides)
        for row in range(5):  # 5 lignes
            for col in range(9):  # 9 colonnes
                placeholder = QWidget()
                placeholder.setStyleSheet("background-color: #e0e0e0; border-radius: 6px;")  # Juste pour voir les cases
                self.home_layout.addWidget(placeholder, row, col)

        # Cell Projets
        cell_projects = QWidget()
        cell_projects.setObjectName("home_cell")
        self.home_layout.addWidget(cell_projects, 0, 0, 2, 6)  # Fusion de 2 lignes x 6 colonnes (positions (0, 0))

        # Cell Note
        self.create_cell_with_button("cell_note", self.on_button_notes_click, (0, 6), rowspan=2, colspan=1)

        # Cell Solarpunk
        self.create_cell_with_button("cell_solarpunk", self.on_button_solarpunk_click, (0, 7), rowspan=1, colspan=2)

        # Cell Gestion de projet
        self.create_cell_with_button("home_cell", self.on_button_gestion_click, (1, 7))

        # Cell Statistique
        self.create_cell_with_button("home_cell", self.on_button_stat_click, (1, 8))

        # Cell Calendrier
        cell_calendrier = QWidget()
        cell_calendrier.setObjectName("home_cell")
        self.home_layout.addWidget(cell_calendrier, 2, 0, 3, 9)  # Positionner la cellule à (0, 6) avec 2 lignes et 1 colonne

        # Applique le layout au widget parent
        self.setLayout(self.home_layout)

    def on_button_notes_click(self):
        """Méthode appelée lorsqu'on clique sur le bouton 'Notes'"""
        self.switch_to_notes_page.emit()  # Déclenche l'événement pour changer de page
        self.change_dropdown_to_notes()

    def on_button_gestion_click(self):
        """Méthode appelée lorsqu'on clique sur le bouton 'Gestion de Projets'"""
        self.switch_to_projects_page.emit()  # Déclenche l'événement pour changer de page
        self.change_dropdown_to_projects()

    def on_button_stat_click(self):
        """Méthode appelée lorsqu'on clique sur le bouton 'Statistiques'"""
        self.switch_to_stats_page.emit()  # Déclenche l'événement pour changer de page
        self.change_dropdown_to_stats()

    def on_button_solarpunk_click(self):
        print("Page Solarpunk")

    def change_dropdown_to_notes(self):
        """Change l'index de la dropdown pour afficher la page des Notes"""
        if hasattr(self, 'parent_widget'):
            self.parent_widget.dropdown.setCurrentIndex(1)  # Notes page
        else:
            print("Erreur : parent_widget non défini")

    def change_dropdown_to_projects(self):
        """Change l'index de la dropdown pour afficher la page des Projets"""
        if hasattr(self, 'parent_widget'):
            self.parent_widget.dropdown.setCurrentIndex(2)  # Projects page
        else:
            print("Erreur : parent_widget non défini")

    def change_dropdown_to_stats(self):
        """Change l'index de la dropdown pour afficher la page des Statistiques"""
        if hasattr(self, 'parent_widget'):
            self.parent_widget.dropdown.setCurrentIndex(3)  # Stats page
        else:
            print("Erreur : parent_widget non défini")

    

    def create_cell_with_button(self, object_name, on_click, grid_pos, rowspan=1, colspan=1):
        cell = QWidget()
        cell.setObjectName(object_name)

        layout = QVBoxLayout(cell)
        button = ButtonIcon(icon_name="arrow_big_Right", style="Button_Secondary_Icon", parent=cell)
        button.clicked.connect(on_click)

        layout.addWidget(button)
        layout.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        row, col = grid_pos
        self.home_layout.addWidget(cell, row, col, rowspan, colspan)
