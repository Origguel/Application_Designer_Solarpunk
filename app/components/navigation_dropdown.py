# app/components/navigation_dropdown.py

from PySide6.QtWidgets import QComboBox

class NavigationDropdown(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 36)
        self.setObjectName("Navigation_Dropdown")
        self.addItems(["Accueil", "Notes", "Projets", "Statistiques"])
