# app/components/home_grid.py
from PySide6.QtWidgets import QWidget, QGridLayout

class HomeGrid(QWidget):
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

        # Fusionner les premières 2 lignes x 6 colonnes en une seule cellule
        cell_projects = QWidget()
        cell_projects.setObjectName("Home_Box")
        self.home_layout.addWidget(cell_projects, 0, 0, 2, 6)  # Fusion de 2 lignes x 6 colonnes (positions (0, 0))

        # Ajouter une cellule 2x1 après la 2x1
        cell_notes = QWidget()
        cell_notes.setObjectName("Home_Box")
        self.home_layout.addWidget(cell_notes, 0, 6, 2, 1)  # Positionner la cellule à (0, 6) avec 2 lignes et 1 colonne

        # Ajouter une cellule 2x1 après la 1x2
        cell_solarpunk = QWidget()
        cell_solarpunk.setObjectName("Home_Box")
        self.home_layout.addWidget(cell_solarpunk, 0, 7, 1, 2)  # Positionner la cellule à (0, 6) avec 2 lignes et 1 colonne

        # Ajouter une cellule 2x1 après la 1x1
        cell_gestion = QWidget()
        cell_gestion.setObjectName("Home_Box")
        self.home_layout.addWidget(cell_gestion, 1, 7, 1, 1)  # Positionner la cellule à (0, 6) avec 2 lignes et 1 colonne

        # Ajouter une cellule 2x1 après la 1x1
        cell_stat = QWidget()
        cell_stat.setObjectName("Home_Box")
        self.home_layout.addWidget(cell_stat, 1, 8, 1, 1)  # Positionner la cellule à (0, 6) avec 2 lignes et 1 colonne

        # Ajouter une cellule 2x1 après la 3x9
        cell_calendrier = QWidget()
        cell_calendrier.setObjectName("Home_Box")
        self.home_layout.addWidget(cell_calendrier, 2, 0, 3, 9)  # Positionner la cellule à (0, 6) avec 2 lignes et 1 colonne

        # Applique le layout au widget parent
        self.setLayout(self.home_layout)
