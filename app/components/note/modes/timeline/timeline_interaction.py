from PySide6.QtCore import QPoint, Qt


class TimelineInteraction:
    def __init__(self, canvas):
        self.canvas = canvas
        self.is_panning = False
        self.last_pos = QPoint()
        self.offset_x = 0  # décalage horizontal

        self.zoom_level = 1.0
        self.min_zoom = 0.65  # ≈ 2 ans
        self.max_zoom = 10.0   # ≈ 2 semaines
        self.base_spacing = 120  # espace entre mois à zoom 1.0

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

    def wheelEvent(self, event):
        angle = event.angleDelta().y()
        zoom_factor = 1.1 if angle > 0 else 0.9
        new_zoom = self.zoom_level * zoom_factor

        if self.min_zoom <= new_zoom <= self.max_zoom:
            # 1. Calculer la date visible actuellement au centre
            center_px = self.canvas.width() // 2
            center_date = self.canvas.get_date_for_x(center_px)

            # 2. Zoom effectif
            old_spacing = self.get_spacing()
            self.zoom_level = new_zoom
            new_spacing = self.get_spacing()

            # 3. Calculer la nouvelle position de cette même date après zoom
            new_center_px = self.canvas.get_x_for_date(center_date)

            # 4. Ajuster l'offset pour que la date reste centrée
            self.offset_x -= (new_center_px - center_px)

            self.canvas.update()


    def get_offset_x(self):
        return self.offset_x

    def get_spacing(self):
        return self.base_spacing * self.zoom_level

    def get_zoom_level(self):
        return self.zoom_level
