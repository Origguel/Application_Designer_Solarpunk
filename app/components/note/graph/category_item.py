from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem
from PySide6.QtGui import QBrush, QPen, QColor
from PySide6.QtCore import QPointF, Qt
import math
import random


class CategoryItem(QGraphicsItem):
    def __init__(self, name, origin_point, scene, radius=20, distance=1000, min_spawn_ratio=0.6):
        super().__init__()

        self.name = name
        self.origin = origin_point           # QPointF : position fixe (point A)
        self.distance = distance             # Distance fixe du lien
        self.radius = radius                 # Rayon du cercle catégorie

        # Position dynamique du point B (initialisée aléatoirement autour de A)
        # Direction parent → centre
        to_origin = QPointF(0, 0) - self.origin
        angle_to_center = math.atan2(to_origin.y(), to_origin.x())

        # Ajouter une variation autour de l'opposé (angle + pi)
        angle = angle_to_center + math.pi + random.uniform(-0.5, 0.5)

        # Rayon variable mais avec minimum garanti
        r = distance * random.uniform(min_spawn_ratio, 0.9)

        self.pos_b = QPointF(
            self.origin.x() + r * math.cos(angle),
            self.origin.y() + r * math.sin(angle)
        )
        self.velocity = QPointF(0, 0)

        # Ligne de liaison A → B
        self.link = QGraphicsLineItem()
        self.link.setPen(QPen(Qt.black, 2))
        scene.addItem(self.link)

        # Cercle au point B
        self.circle = QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
        self.circle.setBrush(QBrush(QColor("white")))
        self.circle.setPen(QPen(Qt.black, 2))
        self.circle.setZValue(1)
        scene.addItem(self.circle)

        # Ajout à la scène (positionné via advance())
        self.scene = scene

    def add_to_velocity(self, dx, dy):
        self.velocity = QPointF(self.velocity.x() + dx, self.velocity.y() + dy)

    def update_physics(self, other_items=[], friction=0.85, repel_strength=500, safe_distance=12, velocity_strenght=0.01):

        self.safe_distance = safe_distance                 # Rayon du cercle catégorie
        self.velocity_strenght = velocity_strenght                 # Rayon du cercle catégorie

        dx = self.pos_b.x() - self.origin.x()
        dy = self.pos_b.y() - self.origin.y()
        current_dist = math.hypot(dx, dy)
        target_dist = self.distance
        if current_dist != 0:
            factor = (target_dist - current_dist) / current_dist
            self.add_to_velocity(dx * factor * velocity_strenght, dy * factor * velocity_strenght)

        # Répulsion entre les autres catégories
        safe_dist = self.radius * safe_distance

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

        # Répulsion du centre (A) vers B
        delta_to_center = self.pos_b - self.origin
        dist_to_center = math.hypot(delta_to_center.x(), delta_to_center.y())
        if dist_to_center < self.radius * 2:
            repel = repel_strength * 2 / (dist_to_center * dist_to_center)
            self.add_to_velocity(
                delta_to_center.x() / dist_to_center * repel,
                delta_to_center.y() / dist_to_center * repel
            )

        # Friction + déplacement
        self.velocity *= friction
        self.pos_b += self.velocity

        # Affichage
        self.circle.setPos(self.pos_b)
        self.link.setLine(self.origin.x(), self.origin.y(), self.pos_b.x(), self.pos_b.y())