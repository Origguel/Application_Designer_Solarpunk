from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class ProjectsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Page de Gestion des Projets"))
        self.setLayout(layout)
