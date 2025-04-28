from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class StatisticsView(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Page de Statistiques"))
        self.setLayout(layout)
