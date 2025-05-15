from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import Qt

class ClickableEllipse:
    def __init__(self, ellipse: QGraphicsEllipseItem, data: dict, parent_widget):
        self.ellipse = ellipse
        self.data = data
        self.parent = parent_widget

        self.normal_brush = self.ellipse.brush()  # 🖌️ Sauvegarder l'état normal
        self.hover_brush = QBrush(QColor("red"))  # 🟥 Brush pour le hover

        self.ellipse.setAcceptHoverEvents(True)
        self.ellipse.setFlag(QGraphicsEllipseItem.ItemIsSelectable, False)  # ❌ On désactive la sélection Qt
        self.ellipse.hoverEnterEvent = self.hover_enter
        self.ellipse.hoverLeaveEvent = self.hover_leave
        self.ellipse.mousePressEvent = self.click

    def hover_enter(self, event):
        self.ellipse.setCursor(Qt.PointingHandCursor)
        self.ellipse.setBrush(self.hover_brush)  # 🟥 Passer en rouge pour debug

    def hover_leave(self, event):
        self.ellipse.setCursor(Qt.ArrowCursor)
        self.ellipse.setBrush(self.normal_brush)  # 🔙 Remettre la couleur normale

    def click(self, event):
        if event.button() == Qt.LeftButton:
            self.parent.show_note_detail(self.data)
