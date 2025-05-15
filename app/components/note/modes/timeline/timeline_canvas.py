from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtCore import Qt, QPoint, QRect
from datetime import datetime, timedelta
from pathlib import Path
import json

from .timeline_interaction import TimelineInteraction
from .items.timeline_note_item import TimelineNoteItem
from .items.timeline_month_item import TimelineMonthItem
from .timeline_data_loader import TimelineDataLoader

class TimelineCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.interaction = TimelineInteraction(self)
        self.visible_months = {}  # Clé = index relatif au mois actuel, valeur = datetime
        self.data_loader = TimelineDataLoader()

    def paintEvent(self, event):
        self.update_visible_months()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        center_x = w // 2
        y_line = self.height() - 128

        # Ligne principale
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(0, y_line, w, y_line)

        offset = self.interaction.get_offset_x()
        spacing = self.interaction.get_spacing()
        font = QFont("Arial", 10)
        painter.setFont(font)

        # Trait orange pour aujourd'hui
        today = datetime.today()
        x_today = self.get_x_for_date(today)
        painter.setPen(QPen(QColor("#EC831E"), 2))
        painter.drawLine(x_today, 0, x_today, self.height())

        # Affichage des notes
        for date_str in self.data_loader.note_index.keys():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                x = self.get_x_for_date(date_obj)
                notes = self.data_loader.get_notes_for_date(date_obj)

                note_items = [TimelineNoteItem(x, y_line, idx, self.interaction.get_zoom_level())
                              for idx, note in reversed(list(enumerate(notes)))]

                for item in note_items:
                    item.draw_line(painter)
                for item in note_items:
                    item.draw_point(painter)

            except Exception as e:
                print(f"Erreur affichage note : {e}")

        # Affichage des mois
        for i, date in self.visible_months.items():
            x = center_x + i * spacing + offset
            item = TimelineMonthItem(x, date, y_line, spacing)
            item.draw(painter)

    def get_x_for_date(self, target_date):
        today = datetime.today()
        base_date = datetime(today.year, today.month, 1)
        delta_days = (target_date - base_date).days

        spacing = self.interaction.get_spacing()
        pixels_per_day = spacing / 30
        center_x = self.width() // 2
        offset = self.interaction.get_offset_x()

        return center_x + delta_days * pixels_per_day + offset

    def get_date_for_x(self, x_pos):
        today = datetime.today()
        base_date = datetime(today.year, today.month, 1)

        spacing = self.interaction.get_spacing()
        pixels_per_day = spacing / 30
        center_x = self.width() // 2
        offset = self.interaction.get_offset_x()

        delta_px = x_pos - center_x - offset
        delta_days = delta_px / pixels_per_day

        return base_date + timedelta(days=delta_days)

    def update_visible_months(self):
        w = self.width()
        spacing = self.interaction.get_spacing()
        center_x = w // 2
        offset = self.interaction.get_offset_x()
        margin = spacing * 2

        today = datetime.today()
        base_month = datetime(today.year, today.month, 1)

        for i in range(-1000, 1000):
            month = (base_month.month - 1 + i) % 12 + 1
            year = base_month.year + ((base_month.month - 1 + i) // 12)
            date = datetime(year, month, 1)
            x = center_x + i * spacing + offset

            if -margin <= x <= w + margin:
                self.visible_months[i] = date
            elif i in self.visible_months:
                del self.visible_months[i]

    def mousePressEvent(self, event):
        self.interaction.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.interaction.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.interaction.mouseReleaseEvent(event)

    def wheelEvent(self, event):
        self.interaction.wheelEvent(event)