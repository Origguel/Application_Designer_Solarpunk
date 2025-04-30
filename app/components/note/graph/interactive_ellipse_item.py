from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt

class InteractiveEllipseItem(QGraphicsEllipseItem):
    selected_item = None

    def __init__(self, rect, data, parent_widget):
        super().__init__(rect)
        self.note_data = data  # ⚡ Renommé pour éviter de casser Qt.data() !!
        self.parent = parent_widget

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)

        self.default_pen = QPen(Qt.black)
        self.default_brush = Qt.black
        self.hover_scale = 1.5
        self.original_rect = rect

        self.setPen(self.default_pen)
        self.setBrush(self.default_brush)

        # 🆕 ENREGISTRER L'ID DANS LE SYSTÈME DE QT CORRECTEMENT
        self.setData(0, self.note_data["id"])

        self.is_search_highlighted = False

    def hoverEnterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)
        if InteractiveEllipseItem.selected_item != self:
            self.scale_up()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        if InteractiveEllipseItem.selected_item != self:
            self.scale_down()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if InteractiveEllipseItem.selected_item and InteractiveEllipseItem.selected_item != self:
                InteractiveEllipseItem.selected_item.deselect()
            InteractiveEllipseItem.selected_item = self
            self.setBrush(QColor("#EC831E"))
            self.scale_up()
            self.parent.show_note_detail(self.note_data)
        super().mousePressEvent(event)

    def deselect(self):
        self.setBrush(self.default_brush)
        self.scale_down()

    def scale_up(self):
        new_rect = self.original_rect.adjusted(
            -self.original_rect.width() * (self.hover_scale - 1) / 2,
            -self.original_rect.height() * (self.hover_scale - 1) / 2,
            self.original_rect.width() * (self.hover_scale - 1) / 2,
            self.original_rect.height() * (self.hover_scale - 1) / 2,
        )
        self.setRect(new_rect)

    def scale_down(self):
        self.setRect(self.original_rect)

    def highlight(self):
        """Mettre en surbrillance le cercle (recherche)"""
        self.setPen(QPen(QColor("#EC831E"), 2))
        self.scale_up()
        self.is_search_highlighted = True

    def remove_highlight(self):
        """Retirer la surbrillance"""
        self.setPen(self.default_pen)
        self.scale_down()
        self.is_search_highlighted = False
