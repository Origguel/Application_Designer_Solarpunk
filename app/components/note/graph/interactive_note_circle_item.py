# app/components/note/graph/interactive_note_circle_item.py

from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush, QColor, QCursor
from PySide6.QtCore import Qt

class InteractiveNoteCircleItem(QGraphicsEllipseItem):
    def __init__(self, note_id, notes_view, parent=None):
        super().__init__(parent)
        self.note_id = note_id
        self.notes_view = notes_view
        self.setAcceptHoverEvents(True)
        self.default_brush = QBrush(Qt.black)
        self.hover_brush = QBrush(QColor("#FF9900"))  # orange au survol
        self.setBrush(self.default_brush)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def hoverEnterEvent(self, event):
        self.setBrush(self.hover_brush)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.default_brush)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        print(f"🖱️ Note cliquée : {self.note_id}")
        self.notes_view.open_note_detail(self.note_id)
        super().mousePressEvent(event)
