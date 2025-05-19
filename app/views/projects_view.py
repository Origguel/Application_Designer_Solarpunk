from PySide6.QtWidgets import QWidget, QMainWindow, QStackedLayout, QGridLayout
import os
import json
from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

# Component
from app.components.project.project_page_widget import ProjectsPageWidget
from app.components.dropdowns.dropdown_default import Dropdown_Default
from app.components.dropdowns.dropdown_legende import Dropdown_Legende


class ProjectsView(QWidget):
    def __init__(self):
        super().__init__()
        # === Conteneur central ===
        self.main_layout = QStackedLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.main_layout.setObjectName("ProjectView")

        self.project_page = ProjectsPageWidget()
        self.main_layout.addWidget(self.project_page)