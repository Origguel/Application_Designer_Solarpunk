from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt, QPoint


class TimelineNoteItem:
    def __init__(self, x, y_line, idx, zoom, canvas=None, note_id=None):
        self.note_id = note_id
        self.canvas = canvas

        self.highlighted = False
        self.selected = False

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
        print(f"🖌️ draw_point : x={self.x} highlighted={self.highlighted} id={id(self)}")
        if self.selected:
            painter.setBrush(QColor("#F18805"))
            painter.setPen(Qt.NoPen)
        elif self.highlighted:
            painter.setBrush(QColor("#F18805"))
            painter.setPen(QPen(Qt.black, 1.5))
        else:
            print(f"⬛ draw_point : normal x={self.x}")
            painter.setBrush(Qt.black)
            painter.setPen(Qt.NoPen)

        painter.drawEllipse(QPoint(self.x, self.note_top), self.radius, self.radius)




    def contains(self, pos):
        dx = pos.x() - self.x
        dy = pos.y() - self.note_top
        inside = dx * dx + dy * dy <= self.radius * self.radius
        print(f"🧪 contains? cursor=({pos.x()},{pos.y()})  note=({self.x},{self.note_top})  inside={inside}")
        return inside


    def set_highlight(self, highlighted: bool):
        self.highlighted = highlighted
        print(f"🎯 set_highlight({highlighted}) pour note x={self.x} id={id(self)}")
        if self.canvas:
            self.canvas.update()




    def set_selected(self, selected: bool):
        self.selected = selected
