from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QFont, QColor
from PySide6.QtCore import Qt, QPoint, QRect
from datetime import datetime, timedelta
from pathlib import Path
import json

from .timeline_interaction import TimelineInteraction

class TimelineCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.interaction = TimelineInteraction(self)
        self.visible_months = {}  # Clé = index relatif au mois actuel, valeur = datetime
        self.note_index = self.load_note_index()
        self.note_cache = {}  # {id: note_data}

    def paintEvent(self, event):
        self.update_visible_months()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        center_x = w // 2
        y_line = self.height() - 128

        # Ligne principale
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(0, y_line, w, y_line)

        # Récupérer l’offset
        offset = self.interaction.get_offset_x()
        spacing = self.interaction.get_spacing()
        radius = 6
        font = QFont("Arial", 10)
        painter.setFont(font)

        # Point de référence = mois actuel
        today = datetime.today()
        current_month = datetime(today.year, today.month, 1)
        total_months = (w // spacing) + 4

        # --- TRAIT ORANGE POUR AUJOURD'HUI ---
        today = datetime.today()
        x_today = self.get_x_for_date(today)

        painter.setPen(QPen(QColor("#EC831E"), 2))
        painter.drawLine(x_today, 0, x_today, self.height())


        # ✅ 1. D'abord afficher les notes
        for date_str in self.note_index.keys():
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                x = self.get_x_for_date(date_obj)
                notes = self.get_notes_for_date(date_obj)

                for idx, note in reversed(list(enumerate(notes))):
                    zoom = self.interaction.get_zoom_level()

                    # Taille dynamique de la hauteur de ligne (entre 30 et 120)
                    line_height = max(30, min(200, int(zoom * 60)))

                    # Espacement vertical dynamique entre les notes (entre 12 et 50)
                    offset_step = max(12, min(50, int(zoom * 12)))
                    offset_y = (idx + 1) * offset_step

                    note_top = y_line - line_height - offset_y
                    note_bottom = y_line

                    # Rayon dynamique du point
                    radius = max(2, min(8, int(zoom * 2)))

                    # Dessin
                    painter.setBrush(Qt.black)
                    painter.drawEllipse(QPoint(x, note_top), radius, radius)

                    painter.setPen(QPen(QColor("#B3B3B3"), 1))
                    painter.drawLine(x, note_top, x, note_bottom)


            except Exception as e:
                print(f"Erreur affichage note : {e}")

        # ✅ 2. Ensuite dessiner les mois par-dessus
        for i, date in self.visible_months.items():
            x = center_x + i * spacing + offset

            painter.setPen(QPen(Qt.black, 2))
            painter.setBrush(Qt.white)
            painter.drawEllipse(QPoint(x, y_line), radius, radius)

            label = date.strftime("%b %Y")
            text_rect = QRect(x - 40, y_line + 12, 80, 20)
            painter.drawText(text_rect, Qt.AlignCenter, label)

            for j in range(1, 4):
                sub_x = x + j * spacing // 4
                painter.setPen(QPen(Qt.gray, 1))
                painter.drawLine(sub_x, y_line - 10, sub_x, y_line + 10)


    def get_x_for_date(self, target_date):
        today = datetime.today()
        base_date = datetime(today.year, today.month, 1)
        delta_days = (target_date - base_date).days

        spacing = self.interaction.get_spacing()
        pixels_per_day = spacing / 30  # approx
        center_x = self.width() // 2
        offset = self.interaction.get_offset_x()

        return center_x + delta_days * pixels_per_day + offset

    def mousePressEvent(self, event):
        self.interaction.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.interaction.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.interaction.mouseReleaseEvent(event)

    def wheelEvent(self, event):
        self.interaction.wheelEvent(event)

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

    def load_note_index(self):
        index_path = Path("data/timeline/note_index_by_date.json")
        if not index_path.exists():
            print("❌ Fichier d'index de notes introuvable")
            return {}
        with open(index_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_notes_for_date(self, date_obj):
        date_str = date_obj.strftime("%Y-%m-%d")
        note_ids = self.note_index.get(date_str, [])
        notes = []
        for note_id in note_ids:
            if note_id in self.note_cache:
                notes.append(self.note_cache[note_id])
            else:
                try:
                    with open(f"data/notes/{note_id}.json", "r", encoding="utf-8") as f:
                        note_data = json.load(f)
                        self.note_cache[note_id] = note_data
                        notes.append(note_data)
                except Exception as e:
                    print(f"❌ Note manquante : {note_id}")
        return notes
    
    def get_date_for_x(self, x_pos):
        today = datetime.today()
        base_date = datetime(today.year, today.month, 1)

        spacing = self.interaction.get_spacing()
        pixels_per_day = spacing / 30
        center_x = self.width() // 2
        offset = self.interaction.get_offset_x()

        # Calcul du nombre de jours depuis base_date
        delta_px = x_pos - center_x - offset
        delta_days = delta_px / pixels_per_day

        return base_date + timedelta(days=delta_days)
