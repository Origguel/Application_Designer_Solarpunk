# app/views/home_view.py
from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QStackedLayout
from app.views.notes_view import NotesView
from app.views.projects_view import ProjectsView
from app.views.statistics_view import StatisticsView

# Components
from app.components.dropdowns.dropdown_default import Dropdown_Default
from app.components.home_grid import HomeGrid  # Import du fichier home_grid.py

class HomeView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accueil - Mon Application")

        # Conteneur principal
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Nouveau layout principal
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(0)

        # Stack de pages
        self.stack_container = QWidget(self.central_widget)
        self.stack_layout = QStackedLayout(self.stack_container)
        self.grid_layout.addWidget(self.stack_container, 0, 0)

        # Pages
        self.notes_page = NotesView()
        self.projects_page = ProjectsView()
        self.statistics_page = StatisticsView()
        self.home_page = self.create_home_page()

        self.stack_layout.addWidget(self.home_page)
        self.stack_layout.addWidget(self.notes_page)
        self.stack_layout.addWidget(self.projects_page)
        self.stack_layout.addWidget(self.statistics_page)

        # Dropdown
        self.dropdown = Dropdown_Default(style="Dropdown_Default", items=["Accueil", "Notes", "Projets", "Statistiques"], responsive=False, parent=self)
        self.dropdown.currentIndexChanged.connect(self.changer_page)
        self.dropdown.raise_()

        # Masquer la dropdown immédiatement au démarrage
        self.hide_dropdown_on_home()

        self.showMaximized()
        self.stack_layout.setCurrentWidget(self.home_page)  # S'assurer que la grille est la première page affichée

        # Connecter les signaux pour changer de page
        self.home_page.switch_to_notes_page.connect(self.switch_to_notes_page)
        self.home_page.switch_to_projects_page.connect(self.switch_to_projects_page)
        self.home_page.switch_to_stats_page.connect(self.switch_to_stats_page)

    def switch_to_notes_page(self):
        """Changer de page vers les notes"""
        self.stack_layout.setCurrentWidget(self.notes_page)

    def switch_to_projects_page(self):
        """Changer de page vers les projets"""
        self.stack_layout.setCurrentWidget(self.projects_page)

    def switch_to_stats_page(self):
        """Changer de page vers les statistiques"""
        self.stack_layout.setCurrentWidget(self.statistics_page)

    def create_home_page(self):
        """Retourne la page contenant la grille de 5x9 cases"""
        home_grid = HomeGrid()
        home_grid.parent_widget = self  # Définir le parent de HomeGrid pour accéder à la dropdown
        return home_grid

    def changer_page(self, index):
        """Changer de page en fonction de l'index sélectionné"""
        self.stack_layout.setCurrentIndex(index)
        self.hide_dropdown_on_home()  # Masquer ou afficher la dropdown en fonction de la page actuelle

    def hide_dropdown_on_home(self):
        """Masque la dropdown dans HomeView et la réaffiche sur les autres pages"""
        if self.stack_layout.currentWidget() == self.home_page:
            self.dropdown.setVisible(False)  # Masquer la dropdown sur la page d'accueil
        else:
            self.dropdown.setVisible(True)  # Afficher la dropdown sur les autres pages

    def resizeEvent(self, event):
        """Adapter la position de la dropdown lors du redimensionnement de la fenêtre"""
        super().resizeEvent(event)
        self.dropdown.move(self.width() - self.dropdown.width() - 34, 26)
