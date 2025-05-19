from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy

# Component
from app.components.project.project_page_widget import ProjectsPageWidget

class ProjectsView(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.project_page = ProjectsPageWidget()
        self.project_page.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.project_page)
