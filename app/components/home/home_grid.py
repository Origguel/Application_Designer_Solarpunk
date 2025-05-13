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

        def create_background_cell(image_path: str, object_name: str = "home_cell") -> QFrame:
            frame = QFrame()
            frame.setObjectName(object_name)
            frame.setStyleSheet(f"""
                QFrame#{object_name} {{
                    border: 1px solid #2B2B2B;
                    border-radius: 6px;
                    background-color: transparent;
                }}
            """)

            label = QLabel(frame)
            label.setScaledContents(True)  # ← important pour forcer le fill sans bug
            pixmap = QPixmap(image_path)
            label.setPixmap(pixmap.scaled(
                frame.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
            ))
            label.setGeometry(0, 0, frame.width(), frame.height())
            label.lower()

            def resize_background():
                label.setPixmap(pixmap.scaled(
                    frame.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                ))
                label.setGeometry(0, 0, frame.width(), frame.height())

            frame.resizeEvent = lambda event: resize_background()

            return frame


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

        # Ajouter une cellule 2x1 après la 2x6
        cell_notes = QWidget()
        cell_notes.setObjectName("cell_note")
        cell_notes_layout = QVBoxLayout(cell_notes)
        button_notes = ButtonIcon(icon_name="arrow_big_Right", style="Button_Secondary_Icon", parent=cell_notes)
        button_notes.clicked.connect(self.on_button_notes_click)
        cell_notes_layout.addWidget(button_notes)
        cell_notes_layout.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(cell_notes, 0, 6, 2, 1)

        # ...
        cell_solarpunk = create_background_cell("assets/img/home_background/solarpunk.png")
        self.home_layout.addWidget(cell_solarpunk, 0, 7, 1, 2)

        # Gestion de Projets (utilise ButtonText)
        cell_gestion = QWidget()
        cell_gestion.setObjectName("Home_Box")
        cell_gestion_layout = QVBoxLayout(cell_gestion)
        button_gestion = ButtonIcon(icon_name="arrow_big_Right", style="Button_Secondary_Icon", parent=cell_gestion)
        button_gestion.clicked.connect(self.on_button_gestion_click)
        cell_gestion_layout.addWidget(button_gestion)
        cell_gestion_layout.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(cell_gestion, 1, 7, 1, 1)

        # Statistiques (utilise ButtonText)
        cell_stat = QWidget()
        cell_stat.setObjectName("Home_Box")
        cell_stat_layout = QVBoxLayout(cell_stat)
        button_stat = ButtonIcon(icon_name="arrow_big_Right", style="Button_Secondary_Icon", parent=cell_stat)
        button_stat.clicked.connect(self.on_button_stat_click)
        cell_stat_layout.addWidget(button_stat)
        cell_stat_layout.setAlignment(Qt.AlignCenter)
        self.home_layout.addWidget(cell_stat, 1, 8, 1, 1)


        # Ajouter d'autres cellules
        cell_calendrier = QWidget()
        cell_calendrier.setObjectName("Home_Box")
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

    
