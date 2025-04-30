from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPen

class DropdownLegendeDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        data = index.data(Qt.UserRole)
        if isinstance(data, dict):
            left_text = data.get("left", "")
            right_text = data.get("right", "")
        else:
            left_text = str(index.data())
            right_text = ""

        painter.save()

        # Hover ou sélection personnalisée
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, Qt.lightGray)  # sélection
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, Qt.color0)  # hover

        # Surcharger avec les couleurs exactes de ton QSS
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, "#D0EFFF")
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, "#E6F7FF")


        # Texte
        painter.setPen(option.palette.text().color())
        rect = option.rect.adjusted(12, 0, -12, 0)
        painter.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, left_text)
        painter.drawText(rect, Qt.AlignVCenter | Qt.AlignRight, right_text)


        painter.restore()
