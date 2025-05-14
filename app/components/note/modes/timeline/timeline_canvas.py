from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QFont
from PySide6.QtCore import Qt, QPoint, QRect
from datetime import datetime, timedelta

from .timeline_interaction import TimelineInteraction

class TimelineCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.months = self.generate_months(center_month=datetime.today(), count=12)
        self.interaction = TimelineInteraction(self)
        self.visible_months = {}  # Clé = index relatif au mois actuel, valeur = datetime



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
        self.update_visible_months()
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w = self.width()
        h = self.height()
        center_x = w // 2
        y_line = h // 2

        # Ligne principale
        painter.setPen(QPen(Qt.black, 2))
        painter.drawLine(0, y_line, w, y_line)

        # Récupérer l’offset
        offset = self.interaction.get_offset_x()

        # Paramètres d'affichage
        spacing = 120  # distance entre mois
        radius = 6
        font = QFont("Arial", 10)
        painter.setFont(font)

        # Point de référence = mois actuel
        today = datetime.today()
        current_month = datetime(today.year, today.month, 1)

        # Combien de mois afficher de chaque côté
        total_months = (w // spacing) + 4  # marge à gauche et droite

        for i, date in self.visible_months.items():
            x = center_x + i * spacing + offset

            # point mois
            painter.setPen(QPen(Qt.darkBlue, 2))
            painter.setBrush(Qt.white)
            painter.drawEllipse(QPoint(x, y_line), radius, radius)

            label = date.strftime("%b %Y")
            text_rect = QRect(x - 40, y_line + 12, 80, 20)
            painter.drawText(text_rect, Qt.AlignCenter, label)

            # traits intermédiaires
            for j in range(1, 4):
                sub_x = x + j * spacing // 4
                painter.setPen(QPen(Qt.gray, 1))
                painter.drawLine(sub_x, y_line - 10, sub_x, y_line + 10)




    def mousePressEvent(self, event):
        self.interaction.mousePressEvent(event)

    def mouseMoveEvent(self, event):
        self.interaction.mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.interaction.mouseReleaseEvent(event)



    def update_visible_months(self):
        """Génère dynamiquement les mois visibles et supprime ceux hors champ."""
        w = self.width()
        spacing = 120
        center_x = w // 2
        offset = self.interaction.get_offset_x()
        margin = spacing * 2  # marge tampon

        # Calculer les bornes d’affichage
        left_bound = -margin
        right_bound = w + margin

        # Point de référence : mois actuel
        today = datetime.today()
        base_month = datetime(today.year, today.month, 1)

        # Générer les mois nécessaires
        for i in range(-1000, 1000):  # Limite raisonnable
            month = (base_month.month - 1 + i) % 12 + 1
            year = base_month.year + ((base_month.month - 1 + i) // 12)
            date = datetime(year, month, 1)
            x = center_x + i * spacing + offset

            if left_bound <= x <= right_bound:
                if i not in self.visible_months:
                    self.visible_months[i] = date
            elif i in self.visible_months:
                del self.visible_months[i]
