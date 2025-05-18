from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt

from app.components.buttons.button_text import ButtonText


class NavigationHeader(QWidget):
    def __init__(self, parent=None, on_nav_callback=None):
        super().__init__(parent)
        self.setObjectName("NavigationHeader")
        self.on_nav_callback = on_nav_callback

        self.buttons = {}

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.setAlignment(Qt.AlignRight | Qt.AlignTop)

        sections = [
            ("Solarpunk", 78),
            ("Statistiques", 87),
            ("Projets", 61),
            ("Notes", 53)
        ]

        for label, width in sections:
            button = ButtonText(label, x=width, parent=self)
            button.clicked.connect(lambda _, s=label: self.handle_click(s))
            layout.addWidget(button)
            self.buttons[label] = button

        self.setLayout(layout)
        self.setFixedHeight(48)

    def handle_click(self, label):
        if self.on_nav_callback:
            self.on_nav_callback(label)

    def highlight(self, section):
        for name, button in self.buttons.items():
            if name == section:
                button.setObjectName("Button_Default_Selected")
            else:
                button.setObjectName("Button_Default")

            button.style().unpolish(button)
            button.style().polish(button)
            button.update()
