from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush, QColor, QCursor
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
        if hasattr(self, "note") and not self.note._selected:
            self.setScale(2.0)
            self.note.label.setScale(1.4)
        super().hoverEnterEvent(event)


    def hoverLeaveEvent(self, event):
        note = getattr(self, "note", None)
        if note:
            if not note._selected:
                self.setScale(1.0)
                note.label.setScale(1.0)
                note.refresh_brush()
        else:
            self.setScale(1.0)
        super().hoverLeaveEvent(event)



    def mousePressEvent(self, event):
        print(f"🖱️ Note cliquée : {self.note_id}")
        if hasattr(self, "note"):
            for item in self.notes_view.graph_widget.note_items:
                item.deselect()
            self.note.select()  # ✅ self.note existe désormais
        self.notes_view.open_note_detail(self.note_id)
        super().mousePressEvent(event)
