from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem, QGraphicsTextItem
from PySide6.QtGui import QBrush, QPen, QColor, QFont
from PySide6.QtCore import QPointF, Qt
import math
import random


class CategoryItem(QGraphicsItem):

    MIN_ZOOM = 0.1
    MAX_ZOOM = 0.2

    def __init__(self, name, parent_ref, scene, radius=20, base_distance=1000, min_spawn_ratio=0.6, angle_hint=None, num_children=0):
        super().__init__()

        self.name = name
        self.parent_ref = parent_ref
        self.radius = radius

        calculated_distance = base_distance + (num_children * 500)
        self.distance = min(max(calculated_distance, base_distance), 10000)

        self.num_children = num_children
        self.safe_multiplier = max(0.2, 4 - math.log2(self.num_children + 1))

        # Angle de direction
        if angle_hint is not None:
            self.angle = angle_hint + random.uniform(-0.3, 0.3)
        else:
            self.angle = random.uniform(0, 2 * math.pi)

        r = self.distance * random.uniform(min_spawn_ratio, 0.9)
        self.pos_b = self.origin() + QPointF(r * math.cos(self.angle), r * math.sin(self.angle))
        self.velocity = QPointF(0, 0)

        self.link = QGraphicsLineItem()
        self.link.setPen(QPen(Qt.black, 2))
        scene.addItem(self.link)

        self.circle = QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
        self.circle.setBrush(QBrush(QColor("white")))
        self.circle.setPen(QPen(Qt.black, 2))
        self.circle.setZValue(1)
        scene.addItem(self.circle)



        # Création du texte du nom de la catégorie
        self.label = QGraphicsTextItem(self.name.upper())
        self.label.setDefaultTextColor(Qt.black)
        font = QFont()
        font.setPointSize(30)  # Taille de police augmentée
        font.setBold(True)
        self.label.setFont(font)
        self.label.setZValue(4)  # S'affiche au-dessus du cercle
        self.label.setParentItem(self.circle)  # Le texte suit le cercle




        self.scene = scene

    def origin(self):
        return self.parent_ref.pos_b if self.parent_ref else QPointF(0, 0)

    def add_to_velocity(self, dx, dy):
        self.velocity = QPointF(self.velocity.x() + dx, self.velocity.y() + dy)

    def update_physics(self, other_items=[], friction=0.8, safe_distance=10, velocity_strenght=0.2):
        self.safe_distance = safe_distance
        self.velocity_strenght = velocity_strenght

        dx = self.pos_b.x() - self.origin().x()
        dy = self.pos_b.y() - self.origin().y()
        current_dist = math.hypot(dx, dy)
        if current_dist != 0:
            factor = (self.distance - current_dist) / current_dist
            self.add_to_velocity(dx * factor * self.velocity_strenght, dy * factor * self.velocity_strenght)

        # 🧠 Repoussement adaptatif selon le nombre de catégories connectées
        base_repel_strength = 1000
        category_count = len(getattr(self.parent_ref, "children", [])) if self.parent_ref else len(other_items)
        category_count = max(category_count, 1)
        repel_strength = base_repel_strength / math.sqrt(category_count)

        safe_dist = self.radius * self.safe_distance * self.safe_multiplier

        for other in other_items:
            if other is self:
                continue
            delta = self.pos_b - other.pos_b
            dist = math.hypot(delta.x(), delta.y())
            if dist < 1:
                dist = 1
            if dist < safe_dist:
                force_factor = 1 - (dist / safe_dist)
                repel_force = repel_strength * (force_factor ** 2)
                self.add_to_velocity(
                    delta.x() / dist * repel_force,
                    delta.y() / dist * repel_force
                )

        delta_to_center = self.pos_b - self.origin()
        dist_to_center = math.hypot(delta_to_center.x(), delta_to_center.y())
        if dist_to_center < self.radius * 2:
            repel = repel_strength * 2 / (dist_to_center * dist_to_center)
            self.add_to_velocity(
                delta_to_center.x() / dist_to_center * repel,
                delta_to_center.y() / dist_to_center * repel
            )

        self.velocity *= friction
        self.pos_b += self.velocity

        origin_pt = self.origin()
        self.circle.setPos(self.pos_b)
        text_rect = self.label.boundingRect()
        self.label.setPos(-text_rect.width() / 2, -self.radius - text_rect.height() - 2)
        self.link.setLine(origin_pt.x(), origin_pt.y(), self.pos_b.x(), self.pos_b.y())



    def update_label_opacity(self, zoom_level):
        zoom = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        normalized = (zoom - self.MIN_ZOOM) / (self.MAX_ZOOM - self.MIN_ZOOM)
        self.label.setOpacity(normalized)

    def update_link_thickness(self, zoom_level):
        zoom = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        normalized = (zoom - self.MIN_ZOOM) / (self.MAX_ZOOM - self.MIN_ZOOM)

        # Inversion : plus le zoom est petit, plus le trait est épais
        min_width = 1
        max_width = 6
        width = max_width - (normalized * (max_width - min_width))

        pen = self.link.pen()
        pen.setWidthF(width)
        self.link.setPen(pen)

    def update_circle_outline_thickness(self, zoom_level):
        zoom = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        normalized = (zoom - self.MIN_ZOOM) / (self.MAX_ZOOM - self.MIN_ZOOM)

        min_width = 1
        max_width = 6
        width = max_width - (normalized * (max_width - min_width))

        pen = self.circle.pen()
        pen.setWidthF(width)
        self.circle.setPen(pen)


    def update_circle_visual_scale(self, zoom_level):
        zoom = max(self.MIN_ZOOM, min(zoom_level, self.MAX_ZOOM))
        normalized = (zoom - self.MIN_ZOOM) / (self.MAX_ZOOM - self.MIN_ZOOM)

        min_scale = 1.0
        max_scale = 2.0
        scale = max_scale - (normalized * (max_scale - min_scale))

        self.circle.setScale(scale)

        # Repositionner le texte au-dessus du cercle (en tenant compte du scale)
        text_rect = self.label.boundingRect()
        offset_y = -self.radius * scale - text_rect.height() - 2
        self.label.setPos(-text_rect.width() / 2, offset_y)
