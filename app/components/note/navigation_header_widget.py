from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import QSize, Qt

class NavigationHeader(QWidget):
    def __init__(self, parent=None, on_nav_callback=None):
        super().__init__(parent)
        self.setObjectName("NavigationHeader")

        self.buttons = {}
        self.on_nav_callback = on_nav_callback


        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        

        sections = ["SOLARPUNK", "STATISTIQUES", "PROJETS", "NOTES"]
        for section in sections:
            button = QPushButton(section)
            button.setObjectName(f"NavButton_{section}")
            button.setCursor(Qt.PointingHandCursor)
            button.setFlat(True)
            button.clicked.connect(lambda checked, s=section: self.handle_click(s))
            layout.addWidget(button)
            self.buttons[section] = button

        self.setLayout(layout)
        self.setFixedHeight(48)

    def handle_click(self, label):
        if self.on_nav_callback:
            self.on_nav_callback(label)

    def highlight(self, section):
        for name, button in self.buttons.items():
            if name == section:
                button.setStyleSheet("font-weight: bold; text-decoration: underline;")
            else:
                button.setStyleSheet("font-weight: normal; text-decoration: none;")
