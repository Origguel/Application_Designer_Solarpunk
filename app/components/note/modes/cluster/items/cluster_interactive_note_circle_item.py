from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush, QColor, QCursor, QPen
from PySide6.QtCore import Qt

class InteractiveNoteCircleItem(QGraphicsEllipseItem):
    def __init__(self, note_id, notes_view, parent=None):
        super().__init__(parent)
        self.note_id = note_id
        self.notes_view = notes_view
        self.setAcceptHoverEvents(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setScale(1.0)  # ✅ important pour pouvoir reset
        self.setBrush(QBrush(Qt.black))  # ✅ reste noir à l’état hover

    def hoverEnterEvent(self, event):
        if self.note and not self.note._selected:
            self.note.circle.setScale(2.0)
            self.note.label.setScale(1.4)
            self.note.refresh_brush()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self.note and not self.note._selected:
            self.note.circle.setScale(1.0)
            self.note.label.setScale(1.0)
        if self.note:
            self.note.refresh_brush()
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        print(f"🖱️ Note cliquée : {self.note_id}")
        if self.note:
            for item in self.notes_view.graph_widget.note_items:
                item.deselect()
            self.note.select()
        self.notes_view.open_note_detail(self.note_id)
        super().mousePressEvent(event)
    