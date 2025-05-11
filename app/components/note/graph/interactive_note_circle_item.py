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
        self.setScale(2.0)
        if hasattr(self.parentItem(), "note"):
            self.parentItem().note.label.setScale(1.4)  # 📈 agrandit texte
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setScale(1.0)
        if hasattr(self.parentItem(), "note"):
            note = self.parentItem().note
            note.label.setScale(1.0)                  # 🔽 texte normal
            note.refresh_brush()                      # 🎨 couleur selon état
        super().hoverLeaveEvent(event)


    def mousePressEvent(self, event):
        print(f"🖱️ Note cliquée : {self.note_id}")
        self.notes_view.open_note_detail(self.note_id)
        super().mousePressEvent(event)
