from PySide6.QtWidgets import QComboBox, QSizePolicy, QStyleOptionComboBox, QStyle
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from app.components.dropdowns.dropdown_legende_delegate import DropdownLegendeDelegate

class Dropdown_Legende(QComboBox):
    def __init__(self, x=200, y=36, style="Dropdown_Default", items=None, legende=None, responsive=False, parent=None):
        super().__init__(parent)
        self.setObjectName(style)
        self.clear()

        if items is None:
            items = ["choix 1", "choix 2", "choix 3", "choix 4"]
        if legende is None:
            legende = ["légende 1", "légende 2", "légende 3", "légende 4"]

        for i in range(min(len(items), len(legende))):
            self.addItem("", {"left": items[i], "right": legende[i]})

        self.setItemDelegate(DropdownLegendeDelegate(self))

        if responsive:
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        else:
            self.setFixedSize(x, y)

    def get_current_data(self):
        return self.currentData()

    def paintEvent(self, event):
        option = QStyleOptionComboBox()
        self.initStyleOption(option)

        painter = QPainter(self)
        try:
            # ✅ Corrigé ici
            self.style().drawComplexControl(QStyle.CC_ComboBox, option, painter, self)

            data = self.currentData()
            if isinstance(data, dict):
                left_text = data.get("left", "")
                right_text = data.get("right", "")
            else:
                left_text = self.currentText()
                right_text = ""

            padding = 12
            text_rect = option.rect.adjusted(padding, 0, -padding - 24, 0)
            painter.setPen(self.palette().text().color())
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, left_text)
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignRight, right_text)

        finally:
            painter.end()
