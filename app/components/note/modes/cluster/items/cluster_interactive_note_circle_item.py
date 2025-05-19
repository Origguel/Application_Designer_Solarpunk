from PySide6.QtWidgets import QGraphicsEllipseItem
from PySide6.QtGui import QBrush, QColor, QCursor, QPen
from PySide6.QtCore import Qt

from app.utils.note_selection_manager import set_selected_note_id

class InteractiveNoteCircleItem(QGraphicsEllipseItem):
    def __init__(self, note_id, notes_view, parent=None):
        super().__init__(parent)
        self.note_id = note_id
        self.notes_view = notes_view
        self.setAcceptHoverEvents(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setScale(1.0)
        self.setBrush(QBrush(Qt.black))

    def hoverEnterEvent(self, event):
        if self.note and not self.note.is_selected():
            self.note.highlight()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self.note and not self.note.is_selected():
            self.note.remove_highlight()
        super().hoverLeaveEvent(event)


    def mousePressEvent(self, event):
        print(f"🖱️ Note cliquée : {self.note_id}")
        set_selected_note_id(self.note_id)
        self.notes_view.graph_widget.refresh_selection_visual()
        self.notes_view.open_note_detail(self.note_id)
        super().mousePressEvent(event)
