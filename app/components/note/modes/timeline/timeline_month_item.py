from PySide6.QtGui import QPen
from PySide6.QtCore import Qt, QPoint, QRect

class TimelineMonthItem:
    def __init__(self, x, date, y_line, spacing):
        self.x = x
        self.date = date
        self.y_line = y_line
        self.spacing = spacing

    def draw(self, painter):
        painter.setPen(QPen(Qt.black, 2))
        painter.setBrush(Qt.white)
        painter.drawEllipse(QPoint(self.x, self.y_line), 6, 6)

        label = self.date.strftime("%b %Y")
        text_rect = QRect(self.x - 40, self.y_line + 12, 80, 20)
        painter.drawText(text_rect, Qt.AlignCenter, label)

        for j in range(1, 4):
            sub_x = self.x + j * self.spacing // 4
            painter.setPen(QPen(Qt.gray, 1))
            painter.drawLine(sub_x, self.y_line - 10, sub_x, self.y_line + 10)
