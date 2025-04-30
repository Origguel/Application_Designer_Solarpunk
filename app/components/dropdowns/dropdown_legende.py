from PySide6.QtWidgets import QComboBox, QSizePolicy

class Dropdown_Legende(QComboBox):
    def __init__(self, x=200, y=36, style="Dropdown_Default", items=None, legende=None, responsive=False, parent=None):
        super().__init__(parent)
        self.setObjectName(style)

        self.clear()

        if items is None:
            items = ["choix 1", "choix 2", "choix 3", "choix 4"]

        if legende is None:
            legende = ["légende 1", "légende 2", "légende 3", "légende 4"]

        # Assure que les deux listes ont la même taille
        min_len = min(len(items), len(legende))

        for i in range(min_len):
            label = f"{items[i]:<20} | {legende[i]}"
            self.addItem(label, userData={"left": items[i], "right": legende[i]})

        if responsive:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:
            self.setFixedSize(x, y)

    def get_current_data(self):
        """Retourne un dictionnaire avec les deux infos du choix actuel"""
        return self.currentData()
