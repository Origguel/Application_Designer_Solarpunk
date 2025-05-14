from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import Qt, QPoint, QRect
from datetime import datetime, timedelta

class TimelineCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.months = self.generate_months(center_month=datetime.today(), count=12)

    def generate_months(self, center_month, count=12):
        """Génère une liste de mois centrée sur le mois actuel."""
        months = []
        mid = count // 2
        for i in range(-mid, mid + 1):
            year = center_month.year + ((center_month.month - 1 + i) // 12)
            month = (center_month.month - 1 + i) % 12 + 1
            months.append(datetime(year, month, 1))
        return months

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        center_x = w // 2
        y_line = h // 2

        # Espace entre les mois (responsif)
        spacing = max(w // (len(self.months) + 2), 100)
        radius = 6
        font = QFont("Arial", 10)
        painter.setFont(font)

        # Ligne principale
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(0, y_line, w, y_line)

        for i, month in enumerate(self.months):
            dx = (i - len(self.months) // 2) * spacing
            x = center_x + dx

            # === Point du mois principal ===
            painter.setPen(QPen(Qt.black, 2))
            painter.setBrush(Qt.white)
            painter.drawEllipse(QPoint(x, y_line), radius, radius)

            # Label du mois
            label = month.strftime("%b %Y")
            text_rect = QRect(x - 40, y_line + 12, 80, 20)
            painter.drawText(text_rect, Qt.AlignCenter, label)

            # === Ajout des 3 traits intermédiaires ===
            if i < len(self.months) - 1:
                next_dx = ((i + 1) - len(self.months) // 2) * spacing
                next_x = center_x + next_dx

                segment_width = next_x - x
                for j in range(1, 4):  # 3 traits pour 4 semaines
                    tick_x = x + (segment_width * j) // 4
                    painter.setPen(QPen(Qt.gray, 1))
                    painter.drawLine(tick_x, y_line - 6, tick_x, y_line + 6)

