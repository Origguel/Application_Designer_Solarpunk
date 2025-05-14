from PySide6.QtWidgets import QWidget, QMainWindow, QStackedLayout, QGridLayout
from PySide6.QtCore import Qt, QPointF

from app.views.projects_view import ProjectsView
from app.views.statistics_view import StatisticsView
from app.components.dropdowns.dropdown_default import Dropdown_Default
from app.components.note.notes_page_widget import NotesPageWidget


class NotesView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Designer Solarpunk")
        self.setObjectName("NotesView")
        self.setStyleSheet("QMainWindow#NotesView { background: white; }")

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

        # === Dropdown ===
        self.dropdown = Dropdown_Default(
            style="Navigation_Dropdown",
            items=["Notes", "Projets", "Statistiques"],
            responsive=False,
            parent=self
        )
        self.dropdown.move(self.width() - self.dropdown.width() - 34, 26)
        self.dropdown.currentIndexChanged.connect(self.changer_page)
        self.dropdown.raise_()

        self.showMaximized()
        self.stack_layout.setCurrentWidget(self.notes_page)

    def changer_page(self, index):
        if index == 0:
            self.stack_layout.setCurrentWidget(self.notes_page)
        elif index == 1:
            self.stack_layout.setCurrentWidget(self.projects_page)
        elif index == 2:
            self.stack_layout.setCurrentWidget(self.statistics_page)

        self.dropdown.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.dropdown.move(self.width() - self.dropdown.width() - 34, 26)
