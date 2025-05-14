# app/components/note/modes/timeline_interaction.py

from PySide6.QtCore import QPoint, Qt

class TimelineInteraction:
    def __init__(self, canvas):
        self.canvas = canvas
        self.is_panning = False
        self.last_pos = QPoint()
        self.offset_x = 0  # Décalage horizontal en pixels

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_panning = True
            self.last_pos = event.pos()


    def mouseMoveEvent(self, event):
        if self.is_panning:
            delta = event.pos().x() - self.last_pos.x()
            self.offset_x += delta
            self.last_pos = event.pos()
            self.canvas.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_panning = False


    def get_offset_x(self):
        return self.offset_x
