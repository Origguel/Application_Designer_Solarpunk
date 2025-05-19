from PySide6.QtWidgets import QWidget, QMainWindow, QStackedLayout, QGridLayout
from PySide6.QtCore import Qt

from app.views.projects_view import ProjectsView
from app.views.statistics_view import StatisticsView
from app.components.note.notes_page_widget import NotesPageWidget
from app.components.note.navigation_header_widget import NavigationHeader


class NotesView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Designer Solarpunk")
        self.setObjectName("NotesView")

        # === Conteneur central ===
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # === Layout principal ===
        self.main_layout = QGridLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # === Stack de vues ===
        self.stack_container = QWidget(self.central_widget)
        self.stack_layout = QStackedLayout(self.stack_container)
        self.main_layout.addWidget(self.stack_container, 0, 0)

        # === Pages ===
        self.notes_page = NotesPageWidget()
        self.projects_page = ProjectsView()
        self.statistics_page = StatisticsView()

        self.stack_layout.addWidget(self.notes_page)
        self.stack_layout.addWidget(self.projects_page)
        self.stack_layout.addWidget(self.statistics_page)

        # === Navigation header personnalisé ===
        self.navbar = NavigationHeader(parent=self, on_nav_callback=self.navigate_to_section)
        self.navbar.resize(297, 32)
        self.navbar.move(self.width() - 297, 16)
        self.navbar.raise_()

        self.showMaximized()
        self.stack_layout.setCurrentWidget(self.notes_page)
        self.navbar.highlight("Notes")

    def navigate_to_section(self, label):
        if label == "Notes":
            self.stack_layout.setCurrentWidget(self.notes_page)
        elif label == "Projets":
            self.stack_layout.setCurrentWidget(self.projects_page)
        elif label == "Statistiques":
            self.stack_layout.setCurrentWidget(self.statistics_page)

        self.navbar.highlight(label)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.navbar.move(
            self.width() - self.navbar.width() - 16,
            16
        )
