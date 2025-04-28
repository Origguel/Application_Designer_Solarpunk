from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QComboBox, QStackedLayout, QGridLayout
)
from PySide6.QtCore import Qt
from app.views.notes_view import NotesView
from app.views.projects_view import ProjectsView
from app.views.statistics_view import StatisticsView
from app.components.navigation_dropdown import NavigationDropdown

from PySide6.QtCore import QFile

fichier = QFile(":/icons/Arrow_Big_Down.svg")
print("Existe ?", fichier.exists())


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

        # Dropdown par-dessus
        self.dropdown = NavigationDropdown(self.central_widget)
        self.dropdown.currentIndexChanged.connect(self.changer_page)
        self.dropdown.raise_()

        self.showMaximized()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Adapter dynamiquement la position de la dropdown
        self.dropdown.move(self.width() - self.dropdown.width() - 34, 26)

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QWidget())  # Vide pour l'instant
        return page

    def changer_page(self, index):
        self.stack_layout.setCurrentIndex(index)
