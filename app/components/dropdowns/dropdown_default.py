from PySide6.QtWidgets import QComboBox, QSizePolicy

class Dropdown_Default(QComboBox):
    def __init__(self, x=200, y=36, style="Dropdown_Default", items=None, responsive=False, parent=None):
        super().__init__(parent)
        self.setObjectName(style)

        if items is None:
            items = ["choix 1", "choix 2", "choix 3", "choix 4"]
        self.addItems(items)

        if responsive:
            # Permet au widget de s'étendre dans les layouts
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:
            self.setFixedSize(x, y)
