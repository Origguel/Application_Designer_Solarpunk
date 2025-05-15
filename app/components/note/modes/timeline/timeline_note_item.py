from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt, QPoint


class TimelineNoteItem:
    def __init__(self, x, y_line, idx, zoom):
        self.x = x
        self.zoom = zoom
        self.idx = idx
        self.y_line = y_line

        # Taille et espacement dynamiques
        self.radius = max(2, min(8, int(zoom * 2)))
        self.line_height = max(30, min(200, int(zoom * 60)))
        self.offset_step = max(12, min(50, int(zoom * 12)))
        self.offset_y = (idx + 1) * self.offset_step

        self.note_top = self.y_line - self.line_height - self.offset_y
        self.note_bottom = self.y_line

    def draw_line(self, painter):
        painter.setPen(QPen(QColor("#B3B3B3"), 1))
        painter.drawLine(self.x, self.note_top, self.x, self.note_bottom)

    def draw_point(self, painter):
        painter.setBrush(Qt.black)
        painter.drawEllipse(QPoint(self.x, self.note_top), self.radius, self.radius)
